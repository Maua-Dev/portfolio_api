from src.shared.infra.external.jwt.jwt_utils import b64url_decode, b64url_encode, is_jwt_shape


class Test_JwtUtils:
    def test_b64url_roundtrip(self):
        raw = b'{"sub":"abc"}'
        encoded = b64url_encode(raw)
        assert "=" not in encoded
        assert b64url_decode(encoded) == raw

    def test_is_jwt_shape_valid(self):
        header = b64url_encode(b'{"alg":"RS256"}')
        payload = b64url_encode(b'{"sub":"1"}')
        signature = b64url_encode(b"sig")
        assert is_jwt_shape(f"{header}.{payload}.{signature}") is True

    def test_is_jwt_shape_invalid(self):
        assert is_jwt_shape("not-a-jwt") is False
        assert is_jwt_shape("a.b") is False
        assert is_jwt_shape("a.b.c.d") is False
