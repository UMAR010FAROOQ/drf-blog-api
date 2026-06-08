from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response")
        status_code = response.status_code if response else 200

        message = ""
        response_data = {
            "success": status_code < 400,
            "message": "",
            "data": None
        }


        if status_code >= 400:
            response_data["message"] = "Something went wrong"
            response_data["errors"] = data
            response_data["data"] = None

        else:
            # Extract message if present
            if isinstance(data, dict) and "message" in data:
                message = data.pop("message")

            response_data["message"] = message
            response_data["data"] = data

        return super().render(response_data, accepted_media_type, renderer_context)