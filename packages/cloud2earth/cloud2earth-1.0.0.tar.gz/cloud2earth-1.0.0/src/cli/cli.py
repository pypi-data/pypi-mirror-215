import logging
import click
import ee

from google.auth.transport.requests import AuthorizedSession
from tqdm import tqdm

from cloud2earth.core import Cloud2Earth
from cloud2earth.helpers import load_tabular


@click.command()
@click.argument('dst')
@click.argument("uris")
def main(dst, uris):
    
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filemode='w',
        filename="errors.log"   
    )

    data = load_tabular(
        filename=uris,
        column='URI'
    )

    session = AuthorizedSession(ee.data.get_persistent_credentials())   

    for uri in tqdm(data):
        c2e = Cloud2Earth(
                dst = dst,
                session=session,
                uri=uri
        )

        response = c2e.post()
        
        if 'error' in response.keys():
            data = response.get('error')
            message = f'error: {data.get("code")}, message: {data.get("message")}:: status {data.get("status")}'
            logging.error(message)

