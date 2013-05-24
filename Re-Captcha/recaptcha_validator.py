import cherrypy
from recaptcha.client import captcha


class Main(object):

    # Display recaptcha form
    @cherrypy.expose
    def display_recaptcha(self, *args, **kwargs):
        public = "6Lf98eASAAAAAMARWX5AXv33iiHwS6E6I3tkVOFT"
        captcha_html = captcha.displayhtml(
            public,
            use_ssl=False,
            error="Something broke!")

        # You'll probably want to add error message handling here if you
        # have been redirected from a failed attempt
        return """
        <form action="validate">
        %s
        <input type=submit value="Submit Captcha Text" \>
        </form>
        """ % captcha_html

    # send the recaptcha fields for validation
    @cherrypy.expose
    def validate(self, *args, **kwargs):
        # these should be here, in the real world, you'd display a nice error
        # then redirect the user to something useful

        if not "recaptcha_challenge_field" in kwargs:
            return "no recaptcha_challenge_field"

        if not "recaptcha_response_field" in kwargs:
            return "no recaptcha_response_field"

        recaptcha_challenge_field = kwargs["recaptcha_challenge_field"]
        recaptcha_response_field = kwargs["recaptcha_response_field"]

        # response is just the RecaptchaResponse container class. You'll need
        # to check is_valid and error_code
        response = captcha.submit(
            recaptcha_challenge_field,
            recaptcha_response_field,
            "6Lf98eASAAAAALOFfNYMQEROO1VqJ9tjbHM9DuB9",
            cherrypy.request.headers["Remote-Addr"],)

        if response.is_valid:
            #redirect to where ever we want to go on success
            raise cherrypy.HTTPRedirect("./success.htm")

        if response.error_code:
            # this tacks on the error to the redirect, so you can let the
            # user knowwhy their submission failed (not handled above,
            # but you are smart :-) )
            raise cherrypy.HTTPRedirect(
                "display_recaptcha?error=%s" % response.error_code)

conf = {'/': {'tools.staticdir.on': True,
        'tools.staticdir.dir': '/Users/amg/python/captchas'}}
cherrypy.quickstart(Main(), '/', config=conf)
