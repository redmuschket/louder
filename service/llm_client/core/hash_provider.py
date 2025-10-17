import bcrypt

class HashProviderService:
    @staticmethod
    def get_hash(data: str) -> str:
        return bcrypt.hashpw(data.encode(), bcrypt.gensalt()).decode()
