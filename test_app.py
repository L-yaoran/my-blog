# -*- coding: utf-8 -*-
import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'AI', resp.data)

    def test_hub(self):
        resp = self.client.get('/hub')
        self.assertEqual(resp.status_code, 200)

    def test_about(self):
        resp = self.client.get('/about')
        self.assertEqual(resp.status_code, 200)

    def test_robots_txt(self):
        resp = self.client.get('/robots.txt')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Sitemap:', resp.data)

    def test_sitemap_xml(self):
        resp = self.client.get('/sitemap.xml')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'<urlset', resp.data)

    def test_static_quiz_pages(self):
        pages = [
            '/static/python_basic_test_001.html',
            '/static/python_basic_test_002.html',
            '/static/python_basic_test_003.html',
            '/static/python_basic_test_004.html',
            '/static/python_basic_test_005.html',
            '/static/python_basic_test_006.html',
            '/static/python_basic_test_007.html',
            '/static/python_basic_test_008.html',
            '/static/python_basic_test_009.html',
        ]
        for path in pages:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 200, '{} returned {}'.format(path, resp.status_code))

    def test_404(self):
        resp = self.client.get('/nonexistent-page')
        self.assertEqual(resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()