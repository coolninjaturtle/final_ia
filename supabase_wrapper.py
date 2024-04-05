import supabase
import os


class SupaBaseWrapper:
    def __init__(self):
        self.__url = "https://gueqnqhycdfkrghaygdk.supabase.co"
        self.__api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1ZXFucWh5Y2Rma3JnaGF5Z2RrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE5NzkzOTgsImV4cCI6MjAyNzU1NTM5OH0.KwZAFTacCjs43ImV8CS0fLzOTTAwl2FYz_THZVbSe-M"

        self.client = supabase.create_client(self.__url, self.__api_key)
        self.auth = self.client.auth

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

    def get_favorite_recipes(self, user_id):
        query = (
            self.client.table("user_recipes")
            .select("recipes(*)")
            .filter("user_id", "eq", user_id)
            .filter("favorited", "eq", "TRUE")
            .execute()
        )

        return query.data

    def insert_new_recipe(self, title, ingredients, process, time, photo):
        photo = self.upload_photo(photo)
        recipe = (
            self.client.table("recipes")
            .insert(
                {
                    "recipe_name": title,
                    "recipe_ingredients": ingredients,
                    "recipe_process": process,
                    "recipe_time": time,
                    "creator": self.current_user.id,
                    "recipe_picture": f"https://gueqnqhycdfkrghaygdk.supabase.co/storage/v1/object/public/recipe_photos/{photo}",
                }
            )
            .execute()
        )
        self.client.table("user_recipes")\
            .insert({"user_id": self.current_user.id, "recipe_id": recipe.data[0]["recipe_id"]}).execute()

    def set_favorite(self, recipe_id, user_id, value):
        self.client.table("user_recipes").update({"favorited": value}).filter(
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
        return query.data[0]["favorited"]

    def edit_recipe(self, title, ingredients, process, recipe_id, photo=None):
        if photo:
            photo = self.upload_photo(photo)
            self.client.table("recipes").update(
                {
                    "recipe_name": title,
                    "recipe_ingredients": ingredients,
                    "recipe_process": process,
                    "recipe_picture": f"https://gueqnqhycdfkrghaygdk.supabase.co/storage/v1/object/public/recipe_photos/{photo}",
                }
            ).filter("recipe_id", "eq", recipe_id).execute()
        else:
            self.client.table("recipes").update(
                {
                    "recipe_name": title,
                    "recipe_ingredients": ingredients,
                    "recipe_process": process,
                }
            ).filter("recipe_id", "eq", recipe_id).execute()

    def upload_photo(self, file):
        with open(file, "rb") as file:
            self.client.storage.from_("recipe_photos").upload(
                file=file, path=os.path.basename(file.name)
            )
        return os.path.basename(file.name)

    def get_recipe_by_id(self, recipe_id):
        query = (
            self.client.table("recipes")
            .select("*")
            .filter("recipe_id", "eq", recipe_id)
            .execute()
        )
        return query.data

    def set_relationship(self, recipe_id, user_id):
        self.client.table("user_recipes").insert(
            {"user_id": user_id, "recipe_id": recipe_id}
        ).execute()

    def sever_relationship(self, recipe_id):
        self.client.table("user_recipes").delete().filter(
            "recipe_id", "eq", recipe_id
        ).filter("user_id", "eq", self.current_user.id).execute()

    def send_feedback(self, user_id, feedback):
        self.client.table("feedback").insert({"user": user_id, "feedback": feedback}).execute()
