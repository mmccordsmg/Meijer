from meijer_funcs import get_meijer_offers, init_meijer_connection_user, strip_tags
import argparse

parser = argparse.ArgumentParser(description="Prints list of Meijer rewards")
parser.add_argument("-u",	"--username",		help="Username (Email address)",		required=True,	type=str)
parser.add_argument("-p",	"--password",		help="Password",										required=True,	type=str)

args = parser.parse_args()

init_meijer_connection_user(args.username, args.password)

for offertype in ['InProgress', 'Available']:
	offers = get_meijer_offers(offertype)
	if offers:
		for offer in offers:
			print(f'{offer.get("meijerOfferId")} - {offer.get("title").strip()} {strip_tags(offer.get("description")).strip()}')