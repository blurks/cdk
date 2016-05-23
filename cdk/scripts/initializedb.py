from __future__ import unicode_literals
import sys

from clld.scripts.util import initializedb, Data, add_language_codes
from clld.db.meta import DBSession
from clld.db.models import common
from clldutils.dsv import UnicodeReader

import cdk
from cdk.scripts.util import load, DIALECTS, PROBLEMS


def main(args):
    data = Data()

    dataset = common.Dataset(
        id=cdk.__name__,
        name="CDK",
        description="Comprehensive Dictionary of Ket",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://www.shh.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='cdk.clld.org',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})

    DBSession.add(dataset)

    contrib = common.Contribution(id='ket', name=dataset.name)
    DBSession.add(contrib)
    for i, (id, name) in enumerate([
        ('kotorov', 'E.G. Kotorova'), ('nefedov', 'A.V. Nefedov'),
    ]):
        dataset.editors.append(
            common.Editor(contributor=common.Contributor(id=id, name=name), ord=i))

    ket = data.add(
        common.Language, 'ket',
        id='ket',
        name='Ket',
        latitude=63.76,
        longitude=87.55)
    add_language_codes(data, ket, 'ket', glottocode='kett1243')
    for abbr, name in DIALECTS.items():
        data.add(common.Language, abbr, id=abbr, name=name)

    with UnicodeReader(args.data_file('Ket_nouns_and_other_pos_table.docx.csv')) as reader:
        load(data, reader, ket, contrib, verbs=False)

    with UnicodeReader(args.data_file('Ket_verbs_table.docx.csv')) as reader:
        load(data, reader, ket, contrib)

    print('parsing examples problematic in %s cases' % len(PROBLEMS))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
