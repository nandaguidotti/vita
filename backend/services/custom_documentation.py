from fastapi.openapi.utils import get_openapi


def customize_documentation(app):
    # Cache the generated schema
    if app.openapi_schema:
        return app.openapi_schema

    # Custom settings
    openapi_schema = get_openapi(
        title="VITA: Visionary Industrial Technology Architecture",
        version="2.1.1",
        description="A modular industrial intelligence platform for 6C integration",
        routes=app.routes,
    )

    # setting new logo to docs
    openapi_schema["info"]["x-logo"] = {
        "url": "https://www.icmc.usp.br/templates/icmc2015/img/logo.png"
    }

    # Override app openapi schema
    app.openapi_schema = openapi_schema
