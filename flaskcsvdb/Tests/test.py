import unittest
from flaskcsvdb.routes import app
from flaskcsvdb.forms import ValidationError



def login(client, email, password):
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

class test_forms(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        print('Test się rozpoczyna')
    def test_successful_login(self):
            with self.client:
                response = login(self.client, email='Nowy10@gmail.com', password='Password10')
                self.assertIn('Jesteś zalogowany!'.encode() , response.data)
            print('Test poprawnego logowania')
    def test_logout(self):
        with self.client:
            logged = login(self.client, email='Nowy10@gmail.com', password='Password10')
            response = logout(self.client)
            self.assertIn('Wylogowałeś się!'.encode(), response.data)
            print("Test poprawnego wylogowania")
    def test_successful_change_prof_data(self):
        with self.client:
            login(self.client, email='Nowy10@gmail.com', password='Password10')
            response = self.client.post('/account',
                                        data=dict(username='Nowy10', email='Nowy10@gmail.com',
                                                  picture='C:/Users/Kacper G/PycharmProjects/Blog/flaskcsvdb/static/profile_pics/index.png'), follow_redirects=True)
            self.assertIn('Zaktualizowano Twój profil!'.encode(), response.data)
            self.assertRaises(ValidationError)
            print('Zmiana danych profilowych')



    def tearDown(self) -> None:
        print("Testy zakończone")

if __name__ == "__main__":
    unittest.main()