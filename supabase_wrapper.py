import supabase


class SupaBaseWrapper:
    def __init__(self):
        self.__url = "https://mbodtpkaammgafckikzs.supabase.co"
        self.__api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1ib2R0cGthYW1tZ2FmY2tpa3pzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDk0ODI2NTYsImV4cCI6MjAyNTA1ODY1Nn0.UU0JLfFobjHyM7APvSc62_2JdseIt0B2VUePhODPcgc"

        self.client = supabase.create_client(self.__url, self.__api_key)
        self.auth = self.client.auth

    def sign_up(self, email, password):
        self.auth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )

    def sign_in(self, email, password):
        self.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )
