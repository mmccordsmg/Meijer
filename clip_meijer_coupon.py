from meijer_funcs import clip_meijer_coupon, init_meijer_connection_user
import argparse

parser = argparse.ArgumentParser(description="Clips specified Meijer coupons for account specified")
parser.add_argument("-u",	"--username",		help="Username (Email address)",		required=True,	type=str)
parser.add_argument("-p",	"--password",		help="Password",										required=True,	type=str)
parser.add_argument("-o",	"--offerid",		help="meijerOfferId to clip",				required=True,	type=str)

args = parser.parse_args()

init_meijer_connection_user(args.username, args.password)

result = clip_meijer_coupon(args.offerid)
if not result == True:
	print ("Error clipping coupon %s - %s" % (args.offerid,  result))
	exit()
else:
	print("Clipped offer %s successfully on account %s." % (args.offerid, args.username))