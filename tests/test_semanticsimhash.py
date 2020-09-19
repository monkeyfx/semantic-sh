import unittest
from contextlib import contextmanager
from semantic_sh import SemanticSimHash
import fasttext.util
import os

class SemanticSimHashBaseTest:

    class BaseTest(unittest.TestCase):

        def setUp(self):
            self.sh = None
            self.docs = ['Super Mario Bros., one of the most influential and best-selling video games of all time, was '
                         'first released for the Nintendo Entertainment System in Japan.',
                         'Scientists confirm the first detection, using gravitational-wave astronomy, of a '
                         'black hole in the upper mass gap.',
                         'As of 13 September 2020, more than 28.7 million cases have been reported worldwide; more '
                         'than 920,000 people have died and more than 19.4 million have recovered.',
                         'Scientists confirm the first detection, using gravitational-wave astronomy, of a '
                         'black hole in the upper mass gap.'
                         ]

        def test_get_encoding(self):
            embs = self.sh._get_encoding(self.docs)

            self.assertEqual(embs.shape, (self.sh.dim, len(self.docs)))

        def test_get_hash(self):
            hashes = self.sh.get_hash(self.docs)
            self.assertEqual(len(hashes), len(self.docs))
            self.assertEqual(hashes[1], hashes[3])

        def test_get_add_document(self):
            hashes, ids = self.sh.add_document(self.docs)
            self.assertEqual(len(hashes), len(self.docs))

        def test_get_distance(self):
            texts = ['He was going to the cinema.', 'He went to the cinema.', 'EU leaders will meet about this issue.']
            low_dist, high_dist = self.sh.get_distance(texts[0], texts[1]), self.sh.get_distance(texts[0], texts[2])

            self.assertGreater(high_dist, low_dist)


class SemanticSimHashBertTest(SemanticSimHashBaseTest.BaseTest):

    def setUp(self):
        super().setUp()
        self.sh = SemanticSimHash(model_type='bert-base-cased', dim=768)


class SemanticSimHashFasttextTest(SemanticSimHashBaseTest.BaseTest):

    def setUp(self):
        super().setUp()
        fasttext.util.download_model('en', if_exists='ignore')
        self.sh = SemanticSimHash(model_path='cc.en.300.bin', model_type='fasttext', dim=300)


class SemanticSimHashGloveTest(SemanticSimHashBaseTest.BaseTest):

    # (ref: https://stackoverflow.com/a/40187331)
    @contextmanager
    def mock_file(self, fname, content=''):
        with open(fname, 'w') as f:
            f.write(content)
        yield fname
        try:
            os.remove(fname)
        except Exception:
            pass

    def setUp(self):
        vec_data = 'she 0.060382 0.37821 -0.75142 -0.72159 0.58648 0.79126 -0.72947 0.68248 -0.12999 -0.22988 0.11595 0.22427 -0.44679 -0.11515 1.0334 -0.088019 -0.78531 0.34305 -0.11457 -0.11905 0.45883 1.6333 0.68546 0.22308 1.0099 -2.6332 -0.52128 0.25665 0.023468 -0.82616 3.1084 0.27219 -0.29227 -0.47259 -0.12297 -0.13545 0.11192 0.86438 0.33121 -0.96616 -0.044785 -0.06674 0.0030367 -0.33905 0.017784 -0.58499 -0.005014 -1.257 -0.060723 0.42247\n' \
                   'he -0.20092 -0.060271 -0.61766 -0.8444 0.5781 0.14671 -0.86098 0.6705 -0.86556 -0.18234 0.15856 0.45814 -1.0163 -0.35874 0.73869 -0.24048 -0.33893 0.25742 -0.78192 0.083528 0.1775 0.91773 0.64531 -0.19896 0.37416 -2.7525 -0.091586 0.040349 -0.064792 -0.31466 3.3944 0.044941 -0.55038 -0.65334 0.10436 0.016394 0.24388 1.0085 0.31412 -0.33806 -0.16925 0.10228 -0.62143 0.19829 -0.36147 -0.24769 -0.38989 -0.33317 -0.041659 -0.013171\n' \
                   'to 0.68047 -0.039263 0.30186 -0.17792 0.42962 0.032246 -0.41376 0.13228 -0.29847 -0.085253 0.17118 0.22419 -0.10046 -0.43653 0.33418 0.67846 0.057204 -0.34448 -0.42785 -0.43275 0.55963 0.10032 0.18677 -0.26854 0.037334 -2.0932 0.22171 -0.39868 0.20912 -0.55725 3.8826 0.47466 -0.95658 -0.37788 0.20869 -0.32752 0.12751 0.088359 0.16351 -0.21634 -0.094375 0.018324 0.21048 -0.03088 -0.19722 0.082279 -0.09434 -0.073297 -0.064699 -0.26044\n' \
                   'the 0.418 0.24968 -0.41242 0.1217 0.34527 -0.044457 -0.49688 -0.17862 -0.00066023 -0.6566 0.27843 -0.14767 -0.55677 0.14658 -0.0095095 0.011658 0.10204 -0.12792 -0.8443 -0.12181 -0.016801 -0.33279 -0.1552 -0.23131 -0.19181 -1.8823 -0.76746 0.099051 -0.42125 -0.19526 4.0071 -0.18594 -0.52287 -0.31681 0.00059213 0.0074449 0.17778 -0.15897 0.012041 -0.054223 -0.29871 -0.15749 -0.34758 -0.045637 -0.44251 0.18785 0.0027849 -0.18411 -0.11514 -0.78581\n' \
                   'cinema 0.081913 0.16832 -0.54545 -0.16228 -0.10527 -0.90241 -0.14241 -1.1414 -0.18878 1.6274 0.38213 -0.28658 -0.071213 0.96138 0.27574 -0.13503 0.42771 1.1297 -0.80078 0.36072 1.5189 0.77558 -0.85977 1.0458 -0.043017 -0.56153 -1.684 -0.17976 -0.84019 -0.040772 1.8722 -0.041814 0.45235 -0.61331 -0.32873 0.1562 0.26638 0.052203 -0.68648 -0.1227 0.33725 0.49107 -0.29965 -0.35219 -0.91063 0.30678 -0.20352 -0.79974 0.18735 0.005643\n' \
                   'was 0.086888 -0.19416 -0.24267 -0.33391 0.56731 0.39783 -0.97809 0.03159 -0.61469 -0.31406 0.56145 0.12886 -0.84193 -0.46992 0.47097 0.023012 -0.59609 0.22291 -1.1614 0.3865 0.067412 0.44883 0.17394 -0.53574 0.17909 -2.1647 -0.12827 0.29036 -0.15061 0.35242 3.124 -0.90085 -0.02567 -0.41709 0.40565 -0.22703 0.76829 0.60982 0.070068 -0.13271 -0.1201 0.096132 -0.43998 -0.48531 -0.5188 -0.3077 -0.75028 -0.77 0.3945 -0.16937\n' \
                   'will 0.81544 0.30171 0.5472 0.46581 0.28531 -0.56112 -0.43913 -0.0090877 0.10002 -0.17218 0.28133 0.37672 -0.40756 0.15836 0.89113 1.2997 0.51508 -0.1948 0.051856 -0.9338 0.069955 -0.24876 -0.016723 -0.2031 -0.033558 -1.8132 0.11199 -0.31961 -0.13746 -0.45499 3.8856 1.214 -1.0046 -0.056274 0.0038776 -0.40669 0.29452 0.30171 0.038848 -0.56088 -0.46582 0.17155 0.33729 -0.15247 0.023771 0.51415 -0.21759 0.31965 -0.34741 0.41672\n' \
                   'going 0.014212 -0.18011 0.23478 -0.25038 0.26816 -0.54887 -0.74436 0.52034 -0.28571 0.15376 -0.55916 0.10423 -1.0179 0.010634 0.9528 0.51811 0.78624 -0.20099 -0.28816 -0.65735 0.018307 0.3193 0.34456 0.26516 0.72061 -1.8699 -0.25384 -0.0030076 1.2203 -0.92019 3.4057 1.1351 -0.58406 -0.12611 -0.035017 -0.29941 0.031475 0.33883 0.3891 -0.42999 -0.85264 -0.31751 -0.089163 0.53176 0.043773 0.060998 0.24762 -0.16679 0.061595 0.69927\n' \
                   'went -0.32756 -0.21984 0.099508 -0.24301 0.22359 -0.25579 -1.5678 0.71203 -0.60978 -0.14974 -0.1801 -0.2335 -0.93444 0.073475 0.65635 -0.20076 -0.2858 -0.30971 -1.0596 0.087789 0.37395 0.45275 0.29004 -0.1191 0.24409 -1.6391 0.25765 -0.20782 0.29576 -0.67762 2.7144 0.43182 -0.23828 0.045421 0.35536 0.022495 0.31211 0.62886 0.42454 -0.017082 -0.53178 -0.12794 -0.23537 0.019563 -0.078219 -0.052478 -0.085261 -0.61849 0.014238 -0.18098\n' \
                   'about 0.89466 0.36604 0.37588 -0.41818 0.58462 0.18594 -0.41907 -0.46621 -0.54903 0.02477 -0.90816 -0.48271 -0.050742 -0.74039 1.4377 -0.01974 -0.2384 0.43154 -0.6612 -0.41275 0.25475 0.93498 0.81404 -0.17296 0.61296 -1.8475 -0.27616 0.27701 0.42347 -0.11599 3.6243 0.12306 -0.023526 -0.24843 -0.22376 -0.53941 -0.62444 -0.27711 0.49406 0.020234 -0.2346 0.44512 0.53397 0.66654 -0.093662 -0.035203 -0.064194 0.55998 -0.66593 0.12177\n' \
                   'issue -0.38155 0.21448 -0.33124 0.10503 0.33547 0.61515 0.034575 -0.42115 0.1065 -0.66252 -0.65648 -0.032601 -0.28544 0.16409 1.0008 0.45067 -0.32211 -0.43219 0.59451 -0.064185 0.7107 0.023696 0.41202 -0.1931 0.3032 -2.1344 -0.096689 0.34065 0.17503 0.42084 3.0067 -0.39575 -0.67946 -0.5203 -0.46329 -0.74343 -0.21211 -0.44892 -0.87834 -0.61563 -0.64452 -0.30718 0.37167 0.30053 -0.30654 0.19544 -0.13802 1.2357 -0.16794 -0.069801\n' \
                   'eu 0.2805 0.096134 -0.40411 -0.43212 -0.21813 0.399 0.11994 -0.58819 0.16138 -0.90326 0.6804 0.079212 -0.207 0.86111 1.0581 0.59307 0.93522 -1.1357 0.91209 -0.73258 0.29839 -0.65858 -0.54395 0.12593 0.0097543 -1.4733 0.99091 0.43032 -0.99453 0.68398 3.0013 0.89257 -1.124 0.37326 -1.1387 -1.0753 -0.093879 0.11037 -0.52445 -0.36921 -0.11846 0.10811 1.6898 -1.2099 -0.35203 0.67106 -0.30708 1.7115 0.2901 -0.41397\n' \
                   'leaders 0.44943 0.15024 -0.037129 -0.22808 0.54271 -0.52404 -0.33716 0.38086 -1.3475 -0.40879 -0.59734 -0.42644 -0.65408 0.45348 -0.27453 -0.11105 0.46486 -0.67978 0.58025 -0.23777 -0.21224 0.35733 0.46048 0.04947 -0.48861 -1.8498 0.18781 -0.63959 -1.1078 0.32185 3.2219 0.9299 -1.3927 -0.66598 -0.22821 -0.70888 -0.69466 -0.46608 -0.88409 0.20053 -0.90601 -0.018557 -0.25097 -0.087047 0.88377 0.53087 -1.176 0.7846 -0.32874 -0.92611'

        with self.mock_file('glove.6B.50d.txt', vec_data):
            self.docs = ['He was going to the cinema.', 'He went to the cinema.',
                         'EU leaders will meet about this issue.', 'He went to the cinema.']
            self.sh = SemanticSimHash(model_path='glove.6B.50d.txt', model_type='glove', dim=50)


if __name__ == '__main__':
    unittest.main()
