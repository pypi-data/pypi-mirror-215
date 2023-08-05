import asyncio
import base64
import json
import secrets
import time
import uuid

from rich.console import Console

from ebsi_wallet.did_jwt import create_jwt
from ebsi_wallet.did_jwt.signer_algorithm import ES256K_signer_algorithm
from ebsi_wallet.did_jwt.util.json_canonicalize.Canonicalize import canonicalize
from ebsi_wallet.ebsi_client import EbsiClient
from ebsi_wallet.siop_auth import Agent
from ebsi_wallet.util import (
    http_call,
    http_call_text,
    http_call_text_redirects_disabled,
    parse_query_string_parameters_from_url,
    verifiable_presentation,
)
from ebsi_wallet.util.verifiable_presentation import create_vp_jwt

console = Console()

app_config = {
    "conformance": {
        "api": "https://api-conformance.ebsi.eu",
        "endpoints": {
            "issuer-initiate-v1": "/conformance/v1/issuer-mock/initiate",
            "issuer-authorize-v1": "/conformance/v1/issuer-mock/authorize",
            "issuer-initiate-v2": "/conformance/v2/issuer-mock/initiate",
            "issuer-authorize-v2": "/conformance/v2/issuer-mock/authorize",
            "issuer-initiate-v3": "/conformance/v3/issuer-mock/initiate",
            "issuer-authorize-v3": "/conformance/v3/issuer-mock/authorize",
            "issuer-token-v1": "/conformance/v1/issuer-mock/token",
            "issuer-token-v2": "/conformance/v2/issuer-mock/token",
            "issuer-token-v3": "/conformance/v3/issuer-mock/token",
            "issuer-credential-v1": "/conformance/v1/issuer-mock/credential",
            "issuer-credential-v2": "/conformance/v2/issuer-mock/credential",
            "issuer-credential-v3": "/conformance/v3/issuer-mock/credential",
            "verifier-auth-request-v1": "/conformance/v1/verifier-mock/authentication-requests",
            "verifier-auth-request-v2": "/conformance/v2/verifier-mock/authentication-requests",
            "verifier-auth-request-v3": "/conformance/v3/verifier-mock/authentication-requests",
            "verifier-auth-response-v1": "/conformance/v1/verifier-mock/authentication-responses",
            "verifier-auth-response-v2": "/conformance/v2/verifier-mock/authentication-responses",
            "verifier-auth-response-v3": "/conformance/v3/verifier-mock/authentication-responses",
        },
        "onboarding": {
            "api": "https://api-conformance.ebsi.eu",
            "endpoints": {
                "post": {
                    "authentication-requests": "/users-onboarding/v1/authentication-requests",
                    "sessions": "/users-onboarding/v1/sessions",
                    "authentication-responses": "/users-onboarding/v1/authentication-responses",
                }
            },
        },
        "authorisation": {
            "api": "https://api-conformance.ebsi.eu",
            "endpoints": {
                "post": {
                    "siop-authentication-requests": "/authorisation/v1/authentication-requests"
                }
            },
        },
        "did": {
            "api": "https://api-conformance.ebsi.eu",
            "endpoints": {"post": {"identifiers": "/did-registry/v2/identifiers"}},
        },
    }
}


async def authorisation(method, headers, options):
    async def siop_request():
        payload = {"scope": "openid did_authn"}

        authReq = await http_call(
            app_config["conformance"]["authorisation"]["api"]
            + app_config["conformance"]["authorisation"]["endpoints"]["post"][
                "siop-authentication-requests"
            ],
            "POST",
            data=payload,
            headers=headers,
        )

        return authReq

    async def siop_session():

        callback_url = options.get("callback_url")
        alg = "ES256K"
        verified_claims = options.get("verified_claims")
        client: EbsiClient = options.get("client")

        nonce = str(uuid.uuid4())
        redirect_uri = callback_url

        public_key_jwk = client.eth.public_key_to_jwk()

        public_key_jwk = {
            "kty": public_key_jwk.get("kty"),
            "crv": public_key_jwk.get("crv"),
            "x": public_key_jwk.get("x"),
            "y": public_key_jwk.get("y"),
        }

        siop_agent = Agent(private_key=client.eth.private_key, did_registry="")

        did_auth_response_jwt = await siop_agent.create_authentication_response(
            client.ebsi_did.did,
            nonce,
            redirect_uri,
            client.eth,
            {"encryption_key": public_key_jwk, "verified_claims": verified_claims},
        )

        updated_headers = {
            **headers,
        }

        data = did_auth_response_jwt["bodyEncoded"]

        authResponses = await http_call(
            callback_url, "POST", data=f"id_token={data}", headers=updated_headers
        )

        return {"alg": "ES256K", "nonce": nonce, "response": authResponses}

    switcher = {"siopRequest": siop_request, "siopSession": siop_session}

    method_fn = switcher.get(method)

    assert method_fn is not None, "Method not found"

    return await method_fn()


async def conformance(method, headers=None, options=None):

    async def issuer_initiate_v3():
        credential_type = options.get("credential_type", "diploma")
        flow_type = options.get("flow_type", "cross-device")
        conformance = options.get("conformance")

        url = (
            app_config["conformance"]["api"]
            + app_config["conformance"]["endpoints"]["issuer-initiate-v3"]
            + f"?credential_type={credential_type}"
            + f"&flow_type={flow_type}"
            + f"&conformance={conformance}"
        )
        response = await http_call_text(url, "GET", data=None, headers=headers)
        return response

    async def issuer_initiate():
        credential_type = options.get("credential_type", "diploma")
        flow_type = options.get("flow_type", "cross-device")
        conformance = options.get("conformance")

        url = (
            app_config["conformance"]["api"]
            + app_config["conformance"]["endpoints"]["issuer-initiate-v2"]
            + f"?credential_type={credential_type}"
            + f"&flow_type={flow_type}"
            + f"&conformance={conformance}"
        )
        response = await http_call_text(url, "GET", data=None, headers=headers)
        return response

    async def issuer_authorize():
        credential_type = options.get("credential_type")

        client: EbsiClient = options.get("client")

        redirect_uri = "https://localhost:3000"

        url_params = {
            "scope": "openid conformance_testing",
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "client_id": redirect_uri
            if client.did_version == "v1"
            else client.ebsi_did.did,
            "response_mode": "post",
            "state": secrets.token_bytes(6).hex(),
        }

        authorize_url = (
            app_config["conformance"]["api"]
            + app_config["conformance"]["endpoints"][
                f"issuer-authorize-{client.did_version}"
            ]
            + "?scope={scope}&response_type={response_type}&redirect_uri={redirect_uri}&client_id={client_id}&response_mode={response_mode}&state={state}"
        )

        if client.did_version == "v2":
            url_params["authorization_details"] = json.dumps(
                [
                    {
                        "type": "openid_credential",
                        "credential_type": credential_type,
                        "format": "jwt_vc",
                    }
                ]
            )

            authorize_url += "&authorization_details={authorization_details}"
        else:
            url_params["nonce"] = secrets.token_bytes(6).hex()
            authorize_url += "&nonce={nonce}"

        if client.did_version == "v2":
            issuer_authorize_response = await http_call_text_redirects_disabled(
                authorize_url.format(**url_params), "GET", data=None, headers=headers
            )
            location = (
                str(issuer_authorize_response).split("Location': '")[1].split("'")[0]
            )
            state = parse_query_string_parameters_from_url(location).get("state")[0]
            code = parse_query_string_parameters_from_url(location).get("code")[0]
            return {"state": state, "code": code}
        else:
            issuer_authorize_response = await http_call(
                authorize_url.format(**url_params), "GET", data=None, headers=headers
            )
            return issuer_authorize_response

    async def issuer_token():
        code = options.get("code")
        did_version = options.get("did_version", "v1")

        redirect_uri = "https://localhost:3000"

        token_url = (
            app_config["conformance"]["api"]
            + app_config["conformance"]["endpoints"][f"issuer-token-{did_version}"]
        )

        payload = {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }

        if did_version == "v2":

            if headers:
                headers["Content-Type"] = "application/x-www-form-urlencoded"

            token_response = await http_call(
                token_url,
                "POST",
                data=f"code={code}&grant_type=authorization_code&redirect_uri={redirect_uri}",
                headers=headers,
            )
            return token_response
        else:

            if headers:
                headers["Content-Type"] = "application/json"

            token_response = await http_call(
                token_url, "POST", data=json.dumps(payload), headers=headers
            )
            return token_response

    async def issuer_credential():
        c_nonce = options.get("c_nonce")
        client: EbsiClient = options.get("client")
        issuer_url = options.get("issuer_url")
        credential_type = options.get("credential_type")

        redirect_uri = options.get("redirect_uri", "https://localhost:3000")

        jwt_payload = None

        if client.did_version == "v1":
            jwt_payload = {"c_nonce": c_nonce}
        else:
            jwt_payload = {"nonce": c_nonce, "aud": issuer_url}

        jwt_payload["iat"] = int(time.time())
        jwt_payload["iss"] = client.ebsi_did.did

        jwt_header = {
            "alg": "ES256K",
            "typ": "JWT",
            "kid": f"{client.ebsi_did.did}#{client.eth.jwk_thumbprint}",
        }

        if client.did_version == "v2":
            public_key_jwk = client.eth.public_key_to_jwk()

            public_key_jwk = {
                "kty": public_key_jwk.get("kty"),
                "crv": public_key_jwk.get("crv"),
                "x": public_key_jwk.get("x"),
                "y": public_key_jwk.get("y"),
            }

            jwt_header["jwk"] = public_key_jwk

        private_key = client.eth.private_key

        jws = await create_jwt(
            jwt_payload,
            {
                "issuer": client.ebsi_did.did,
                "signer": await ES256K_signer_algorithm(private_key),
            },
            jwt_header,
            exp=False,
            canon=False,
        )

        if client.did_version == "v1":

            if headers:
                headers["Content-Type"] = "application/json"

            credential_url = (
                "https://api-conformance.ebsi.eu/conformance/v1/issuer-mock/credential"
            )

            payload = {
                "type": "https://api.test.intebsi.xyz/trusted-schemas-registry/v1/schemas/0x1ee207961aba4a8ba018bacf3aaa338df9884d52e993468297e775a585abe4d8",
                "format": "jwt_vc",
                "did": client.ebsi_did.did,
                "proof": {
                    "type": "JWS",
                    "verificationMethod": f"{client.ebsi_did.did}#keys-1",
                    "jws": jws,
                },
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            }

            credential_response = await http_call(
                credential_url, "POST", data=json.dumps(payload), headers=headers
            )

            return credential_response

        else:

            if headers:
                headers["Content-Type"] = "application/x-www-form-urlencoded"

            credential_url = (
                app_config["conformance"]["api"]
                + app_config["conformance"]["endpoints"][
                    f"issuer-credential-{client.did_version}"
                ]
            )

            payload_str = (
                f"type={credential_type}&proof[proof_type]=jwt&proof[jwt]={jws}"
            )

            credential_response = await http_call(
                credential_url, "POST", data=payload_str, headers=headers
            )

            return credential_response

    async def verifier_auth_request():

        did_version = options.get("did_version")

        url_params = {
            "redirect": "undefined",
        }

        authentication_requests_url = (
            app_config["conformance"]["api"]
            + app_config["conformance"]["endpoints"][
                f"verifier-auth-request-{did_version}"
            ]
            + "?redirect={redirect}"
        )

        authentication_requests_response = await http_call_text(
            authentication_requests_url.format(**url_params),
            "GET",
            data=None,
            headers=headers,
        )
        uri_decoded = authentication_requests_response.replace("openid://", "")

        if did_version == "v1":

            authentication_requests_response = {
                "request": parse_query_string_parameters_from_url(uri_decoded).get(
                    "request"
                )[0],
                "client_id": parse_query_string_parameters_from_url(uri_decoded).get(
                    "client_id"
                )[0],
                "response_type": parse_query_string_parameters_from_url(
                    uri_decoded
                ).get("response_type")[0],
                "scope": parse_query_string_parameters_from_url(uri_decoded).get(
                    "scope"
                )[0],
                "claims": parse_query_string_parameters_from_url(uri_decoded).get(
                    "claims"
                )[0],
            }

            return authentication_requests_response

        else:

            authentication_requests_response = {
                "client_id": parse_query_string_parameters_from_url(uri_decoded).get(
                    "client_id"
                )[0],
                "response_type": parse_query_string_parameters_from_url(
                    uri_decoded
                ).get("response_type")[0],
                "scope": parse_query_string_parameters_from_url(uri_decoded).get(
                    "scope"
                )[0],
                "claims": parse_query_string_parameters_from_url(uri_decoded).get(
                    "claims"
                )[0],
                "redirect_uri": parse_query_string_parameters_from_url(uri_decoded).get(
                    "redirect_uri"
                )[0],
                "nonce": parse_query_string_parameters_from_url(uri_decoded).get(
                    "nonce"
                )[0],
            }

            return authentication_requests_response

    async def verifier_auth_response():
        jwt_vp = options.get("jwtVp")
        client: EbsiClient = options.get("client")

        authentication_response_url = (
            app_config["conformance"]["api"]
            + app_config["conformance"]["endpoints"][
                f"verifier-auth-response-{client.did_version}"
            ]
        )

        if client.did_version == "v1":
            payload = {
                "id_token": {},
                "vp_token": [{"format": "jwt_vp", "presentation": jwt_vp}],
            }

            vp_status = await http_call(
                authentication_response_url,
                "POST",
                data=json.dumps(payload),
                headers=headers,
            )

            return vp_status
        else:
            jwt_payload = {
                "_vp_token": {
                    "presentation_submission": {
                        "id": str(uuid.uuid4()),
                        "definition_id": "conformance_mock_vp_request",
                        "descriptor_map": [
                            {
                                "id": "conformance_mock_vp",
                                "format": "jwt_vp",
                                "path": "$",
                            },
                        ],
                    },
                },
            }

            jwt_header = {
                "alg": "ES256K",
                "typ": "JWT",
                "kid": f"{client.ebsi_did.did}#{client.eth.jwk_thumbprint}",
            }

            public_key_jwk = client.eth.public_key_to_jwk()

            public_key_jwk = {
                "kty": public_key_jwk.get("kty"),
                "crv": public_key_jwk.get("crv"),
                "x": public_key_jwk.get("x"),
                "y": public_key_jwk.get("y"),
            }

            jwt_header["jwk"] = public_key_jwk

            private_key = client.eth.private_key

            id_token = await create_jwt(
                jwt_payload,
                {
                    "issuer": client.ebsi_did.did,
                    "signer": await ES256K_signer_algorithm(private_key),
                },
                jwt_header,
                exp=False,
                canon=False,
            )

            headers["Content-Type"] = "application/x-www-form-urlencoded"

            payload_str = f"id_token={id_token}&vp_token={jwt_vp}"

            vp_status = await http_call(
                authentication_response_url, "POST", data=payload_str, headers=headers
            )

            return vp_status

    switcher = {
        "issuerInitiate": issuer_initiate,
        "issuerInitiateV3": issuer_initiate_v3,
        "issuerAuthorize": issuer_authorize,
        "issuerToken": issuer_token,
        "issuerCredential": issuer_credential,
        "verifierAuthRequest": verifier_auth_request,
        "verifierAuthResponse": verifier_auth_response,
    }

    method_fn = switcher.get(method)

    assert method_fn is not None, "Method not found"

    return await method_fn()


async def compute(method, headers={}, options={}):
    async def create_presentation():

        vc = options.get("vc")

        assert vc is not None, "No VC found"

        vc = json.loads(vc)

        client: EbsiClient = options.get("client")

        assert client is not None, "No client found"

        vp = await verifiable_presentation.create_vp(
            client,
            "ES256K",
            vc,
            {
                "issuer": client.ebsi_did.did,
                "signer": await ES256K_signer_algorithm(client.eth.private_key),
            },
        )

        return vp

    async def canonicalize_base64_url():

        vp = options.get("vp")

        assert vp is not None, "No VP found"

        vp = json.loads(vp)

        encoded = base64.urlsafe_b64encode(canonicalize(vp))

        return encoded.decode("utf-8")

    async def verify_authentication_request():

        request = options.get("request")
        client: EbsiClient = options["client"]

        siop_agent = Agent(
            private_key=client.eth.private_key,
            did_registry=app_config["conformance"]["did"]["api"]
            + app_config["conformance"]["did"]["endpoints"]["post"]["identifiers"],
        )

        await siop_agent.verify_authentication_request(request.get("request"))

        return request["client_id"]

    async def verify_session_response():

        session_response = options.get("session_response")

        client: EbsiClient = options.get("client")

        siop_agent = Agent(
            private_key=client.eth.private_key,
            did_registry=app_config["conformance"]["did"]["api"]
            + app_config["conformance"]["did"]["endpoints"]["post"]["identifiers"],
        )

        access_token = await siop_agent.verify_authentication_response(
            session_response.get("response"), session_response.get("nonce"), client
        )

        return access_token

    async def create_presentation_jwt():
        credential = options.get("credential")
        client: EbsiClient = options.get("client")
        audience = options.get("audience")

        config = {
            "client": client,
            "issuer": client.ebsi_did.did,
            "signer": await ES256K_signer_algorithm(client.eth.private_key),
        }

        vp_jwt_res = await create_vp_jwt(credential, config, audience)

        return vp_jwt_res

    switcher = {
        "createPresentation": create_presentation,
        "canonicalizeBase64url": canonicalize_base64_url,
        "verifyAuthenticationRequest": verify_authentication_request,
        "verifySessionResponse": verify_session_response,
        "createPresentationJwt": create_presentation_jwt,
    }

    method_fn = switcher.get(method)

    assert method_fn is not None, "Method not found"

    return await method_fn()


async def wallet(method):
    async def init():

        client = EbsiClient()
        client.ebsi_did.generate_did()

        return client

    async def init_v2():

        client = EbsiClient(did_version="v2")
        client.ebsi_did.generate_did(eth=client.eth)

        return client

    switcher = {"init": init, "init_v2": init_v2}

    method_fn = switcher.get(method)

    assert method_fn is not None, "Method not found"

    return await method_fn()


async def onboarding(method, headers, options=None):
    async def authentication_requests():
        payload = {"scope": "ebsi users onboarding"}

        authReq = await http_call(
            app_config["conformance"]["onboarding"]["api"]
            + app_config["conformance"]["onboarding"]["endpoints"]["post"][
                "authentication-requests"
            ],
            "POST",
            data=payload,
            headers=headers,
        )

        return authReq

    async def authentication_responses():

        client = options["client"]

        nonce = str(uuid.uuid4())
        redirect_uri = (
            app_config["conformance"]["onboarding"]["api"]
            + app_config["conformance"]["onboarding"]["endpoints"]["post"][
                "authentication-responses"
            ]
        )

        siop_agent = Agent(private_key=client.eth.private_key, did_registry="")

        did_auth_response_jwt = await siop_agent.create_authentication_response(
            client.ebsi_did.did, nonce, redirect_uri, client.eth
        )

        updated_headers = {
            **headers,
        }

        data = did_auth_response_jwt["bodyEncoded"]
        url = did_auth_response_jwt["urlEncoded"]

        authResponses = await http_call(
            url, "POST", data=f"id_token={data}", headers=updated_headers
        )

        return authResponses

    switcher = {
        "authenticationRequests": authentication_requests,
        "authenticationResponses": authentication_responses,
    }

    method_fn = switcher.get(method)

    assert method_fn is not None, "Method not found"

    return await method_fn()


async def main():

    # Visit https://app.preprod.ebsi.eu/users-onboarding to obtain session token.

    headers = {
        "Conformance": str(uuid.uuid4()),
        "Authorization": "Bearer eyJhbGciOiJFUzI1NksiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2NTIxMDk3NzcsImlhdCI6MTY1MjEwODg3NywiaXNzIjoiZGlkOmVic2k6emNHdnFnWlRIQ3Rramd0Y0tSTDdIOGsiLCJvbmJvYXJkaW5nIjoicmVjYXB0Y2hhIiwidmFsaWRhdGVkSW5mbyI6eyJhY3Rpb24iOiJsb2dpbiIsImNoYWxsZW5nZV90cyI6IjIwMjItMDUtMDlUMTU6MDc6NTVaIiwiaG9zdG5hbWUiOiJhcHAucHJlcHJvZC5lYnNpLmV1Iiwic2NvcmUiOjAuOSwic3VjY2VzcyI6dHJ1ZX19.wWPb9xofcgeD3G9J3hShqHOMX-Quvr2kgqw_GXk9ABbYe-YngKojO76ZxkGDBuykkbIP261Gqv5KQLSnSsyRLA",
    }

    # Setup wallet
    client = await wallet("init")

    # Onboarding service

    # Authentication requests
    auth_req = await onboarding("authenticationRequests", headers)
    console.log("Onboarding Service -- Authentication Requests", auth_req)

    session_token = auth_req["session_token"].replace("openid://", "")
    jwt_auth_req = parse_query_string_parameters_from_url(session_token).get("request")[
        0
    ]
    assert jwt_auth_req is not None, "No JWT authentication request found"

    headers = {
        "Authorization": f"Bearer {jwt_auth_req}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Authentication responses
    vc = await onboarding(
        "authenticationResponses",
        headers,
        options={"client": client, "jwt_auth_req": jwt_auth_req},
    )
    console.log("Onboarding Service -- Authentication Responses", vc)

    # Get access token
    vp = await compute(
        "createPresentation",
        None,
        options={"client": client, "vc": json.dumps(vc["verifiableCredential"])},
    )
    console.log("Onboarding Service -- Create Presentation", vp)

    vp_base64 = await compute(
        "canonicalizeBase64url", None, options={"vp": json.dumps(vp)}
    )
    console.log("Onboarding Service -- Canonicalize Base64 URL", vp_base64)

    headers = {
        "Authorization": f"Bearer {jwt_auth_req}",
    }

    siop_auth_request = await authorisation("siopRequest", headers, None)
    console.log("Authorisation Service -- Siop Request", siop_auth_request)

    uri_decoded = siop_auth_request["uri"].replace("openid://", "")
    siop_auth_request_prepared = {
        "request": parse_query_string_parameters_from_url(uri_decoded).get("request")[
            0
        ],
        "client_id": parse_query_string_parameters_from_url(uri_decoded).get(
            "client_id"
        )[0],
    }

    callback_url = await compute(
        "verifyAuthenticationRequest",
        None,
        {"client": client, "request": siop_auth_request_prepared},
    )
    console.log("Authorisation Service -- Verify Authentication Request", callback_url)

    headers = {
        "Authorization": f"Bearer {jwt_auth_req}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    session_response = await authorisation(
        "siopSession",
        headers,
        options={
            "client": client,
            "callback_url": callback_url,
            "verified_claims": vp_base64,
        },
    )
    console.log("Authorisation Service -- Siop Session", session_response)

    access_token = await compute(
        "verifySessionResponse",
        None,
        {"client": client, "session_response": session_response},
    )
    console.log(
        "Authorisation Service -- Verify Session Response -- Access Token", access_token
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
