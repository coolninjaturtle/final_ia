import supabase
from typing import Optional


class SupaBaseWrapper:
    def __init__(self):
        self.__url = "https://gueqnqhycdfkrghaygdk.supabase.co"
        self.__api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1ZXFucWh5Y2Rma3JnaGF5Z2RrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE5NzkzOTgsImV4cCI6MjAyNzU1NTM5OH0.KwZAFTacCjs43ImV8CS0fLzOTTAwl2FYz_THZVbSe-M"

        self.client = supabase.create_client(self.__url, self.__api_key)
        self.auth = self.client.auth
        self.current_user = None

    def sign_up(self, email, password):
        try:
            self.auth.sign_up({"email": email, "password": password})
            self.current_user = self.auth.get_user().user
            return "success"
        except Exception as e:
            return str(e)

    def sign_in(self, email, password):
        try:
            self.auth.sign_in_with_password({"email": email, "password": password})
            self.current_user = self.auth.get_user().user
            return "success"
        except Exception as e:
            return str(e)

    def get_all_recipes(self, user_id):
        query = (
            self.client.table("user_recipes")
            .select("recipes(*)")
            .filter("user_id", "eq", user_id)
            .execute()
        )

        return query.data

    def insert_new_recipe(
        self, title, ingredients, process, user_id, time, photo: Optional[str] = None
    ):
        recipe = (
            self.client.table("recipes")
            .insert(
                {
                    "recipe_name": title,
                    "recipe_ingredients": ingredients,
                    "recipe_process": process,
                    "recipe_time": time,
                    "creator": user_id,
                    "recipe_picture": photo,
                }
            )
            .execute()
        )
        self.client.table("user_recipes").insert(
            {"user_id": user_id, "recipe_id": recipe.data[0]["recipe_id"]}
        ).execute()

    def set_favorite(self, recipe_id, user_id, value):
        self.client.table("user_recipes").update({"favorite": value}).filter(
            "recipe_id", "eq", recipe_id
        ).filter("user_id", "eq", user_id).execute()

    def is_favorite(self, recipe_id, user_id):
        query = (
            self.client.table("user_recipes")
            .select("*")
            .filter("recipe_id", "eq", recipe_id)
            .filter("user_id", "eq", user_id)
            .execute()
        )
        return query[0]["favorite"]
