import os
import logging
import pandas as pd

import ee
from google.auth.transport.requests import AuthorizedSession
from src.cloud2earth.core import Cloud2Earth
from src.cloud2earth.helpers import load_tabular

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='w',
    filename="errors.log"
)

def test_c2e():
    csv = "./data/aoi_novascotia_PathValidation.csv"
    
    data = load_tabular(
        filename=csv,
        column='URI'
    )

    session = AuthorizedSession(ee.data.get_persistent_credentials())   

    c2e1 = Cloud2Earth(
            dst = "projects/fpca-336015/assets/testCollection",
            session=session,
            uri=uris[0]
    )

    response = c2e1.post()
    
    if 'error' in response.keys():
        data = response.get('error')
        message = f'error: {data.get("code")}, message: {data.get("message")}:: status {data.get("status")}'
        logging.error(message)

    c2e2 = Cloud2Earth(
            dst = "projects/fpca-336015/assets/testCollection",
            session=session,
            uri=uris[1]
        )
    b = ' '
        

if __name__ == '__main__':
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    test_c2e()