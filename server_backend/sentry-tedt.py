from raven import Client

client = Client('http://d202ee7ccbea457c8c3707dbe495c978:4e18c5a3693b493fb149723f671dc2ca@sentry.whf.com/2')

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()
