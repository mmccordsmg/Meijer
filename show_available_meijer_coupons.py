from meijer_funcs import get_all_meijer_coupons, init_meijer_connection_user
import argparse

parser = argparse.ArgumentParser(description="Shows all available Meijer coupons for account specified")
parser.add_argument("-u",	"--username",		help="Username (Email address)",		required=True,	type=str)
parser.add_argument("-p",	"--password",		help="Password",										required=True,	type=str)
parser.add_argument("-l",	"--logfile",		help="Logfile name",								required=False,	type=str)


args = parser.parse_args()

if args.logfile:
	logfile = open(args.logfile, 'a')
else:
	logfile = None

init_meijer_connection_user(args.username, args.password)

coupons = get_all_meijer_coupons()
for coupon in coupons:
	print(f'{coupon.get("meijerOfferId")} - {coupon.get("title").strip()} {coupon.get("description").strip()}')
	if logfile:
		logfile.write(f'{args.username} - {coupon.get("meijerOfferId")} - {coupon.get("title").strip()} {coupon.get("description").strip()}')