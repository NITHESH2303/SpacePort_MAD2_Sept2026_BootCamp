# TokenRefresh removed intentionally.
# Will be added properly in a later session when Vue's fetchWithAuth() needs it.
# The correct pattern: refresh_token lives in HttpOnly cookie (set by login),
# Vue sends it automatically via credentials:"include", backend reads the cookie.
# That full flow is built when we wire up fetchWithAuth() on the frontend.