import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from question_app.models import Answer
from student_app.models import Student, Result
from question_app.models import Teacher, Faculty, Question
from question_app.models import Kafedra


def create_faculty(faculties):
    for faculty in faculties:
        Faculty.objects.get_or_create(name=faculty)

def create_kafedra(faculty, kafedralar):
    faculty = Faculty.objects.get(name=faculty)
    for kafedra in kafedralar:
        Kafedra.objects.get_or_create(name=kafedra, faculty=faculty)


def create_teacher(teachers):
    for kafedra in teachers:
        k = Kafedra.objects.get(name=kafedra)
        for teacher in teachers[kafedra]:
            Teacher.objects.get_or_create(name=teacher, kafedra=k)



def create_question(questions):
    for question in questions:
        Question.objects.get_or_create(name=question)


def create_answer(answers):
    for question in answers.keys():
        q = Question.objects.get(name=question)
        mark = 0
        for answer in answers[question]:
            if mark == 0:
                Answer.objects.get_or_create(name=answer, question=q, mark__name=100)
            else:
                Answer.objects.get_or_create(name=answer, question=q, mark__name=0)



if __name__ == "__main__":
    # fakultetlar = ["Math", "Boshqalar"]
    # create_faculty(fakultetlar)

    # matematika_kafedralari = ['Matematik analiz kafedrasi', 'Algebra va funktsional analiz kafedrasi', 'Differentsial tenglamalar kafedrasi', 'Geometriya kafedrasi', 'Ehtimollar nazariyasi kafedrasi', 'Mekhanika kafedrasi']
    # create_kafedra("Math", matematika_kafedralari)

    # boshqa_kafedralar = ['O’zbekistonning eng yangi tarixi kafedrasi', 'Ingliz tili kafedrasi', 'Rus tili kafedrasi', 'Jismoniy tarbiya kafedrasi', 'O’zbek tili kafedrasi', 'Umumiy fizika kafedrasi', 'Amaliy matematika kafedrasi', 'Dasturlash asoslari kafedrasi', 'Olimova Muxlisa kafedrasi', 'Umumiy peagogika va psixologiya kafedrasi', 'Yosh fizoiologiyasi va geginya kafedrasi']
    # create_kafedra("Boshqalar", boshqa_kafedralar)


    # math_teachers = {
    #     "Matematik analiz kafedrasi": [
    #         "Xudoiberganov Gulmirza",
    #         "Shoimqulov Baxodir",
    #         "Tishabayev Juraboy Karimovich",
    #         "Rahimov Karim Xoshimovich",
    #         "Lyan Grigoriy Mihaylovich",
    #         "Toychiev Tahir Tursunboevich",
    #         "Aliqulov Eshpo'lat Omonovich",
    #         "Akromov Nurali",
    #         "Eshimbetov Mardonbek Rejimboevich",
    #         "Otaboyev Tolib O'rolovich",
    #         "Qul'doshov Qobiljon Qul'doshevich",
    #         "Tirkasheva Gulasal Diyor qizi",
    #         "Jumaboyev Rajabbay Sheripboyevich",
    #         "Ergashev Ro'zimurod",
    #         "Nematullaeva Mukhoyo",
    #         "Karimov Zhasurbek Alisherovich",
    #         "Narzullaev Nurbek Chamroqulovich",
    #         "Rahimov Kamoliddin O'rinbaevich",
    #         "Karimov Javlon Jo'raboy o'g'li",
    #         "Imomqulov Sevdiyor",
    #         "Rajabov Suyunjon",
    #         "Boymurodov Sobir",
    #         "Qalandarova Dildora",
    #         "Erkinboev Qutlimurod",
    #         "Qurbonboev Suqrot"
    #     ],
    #     "Algebra va funktsional analiz kafedrasi": [
    #         "Omirov Baxrom Abdazovich",
    #         "Ganixojayev Rasul Nabiyevich",
    #         "Mominov Qobiljon Qodirovich",
    #         "Rahimov Abdug'ofur Abdumadjidovich",
    #         "Kurganov Karim Ayxodjayevich",
    #         "Ibroximov Farxodjon Nurmuhamadjonovich",
    #         "Normatov Erkin Panjievich",
    #         "Kucharov Ramziddin Ruzimuradovich",
    #         "Usmonov Javokhir Baxodir o'gli",
    #         "G'aybullaev Rustamjon Qahramonovich",
    #         "Azizov Azizxon Nodirxon o'gli",
    #         "Solijanova Gulxayo Oybek qizi",
    #         "Shoymardonov S.K",
    #         "Mavlonov Ismoil Muradulla o'gli",
    #         "Chorieva Iroda Baxriddin qizi",
    #         "Karimov Ulug'bek Shokirovich",
    #         "Ayupov Shavkat Abdulloevich",
    #         "Roziqov O'tkir Abdulloevich",
    #         "Jamilov Uyg'un Umirovich",
    #         "Xudoiberdiev Abror Xakimovich",
    #         "Haydarov Farhod Halimjonovich",
    #         "Eshimbetov Muzaffar Rejimbaevich"
    #     ],
    #     "Differentsial tenglamalar kafedrasi": [
    #         "Xalmuxamedov Alimj'an",
    #         "Islomov Bozor",
    #         "Kasimov Shakirbay",
    #         "Mamadaliev Numanjon",
    #         "Buvaev Qahramon",
    #         "Fayziev Yusuf",
    #         "Alikulov Tolib",
    #         "Qo'cho'rov Erkin",
    #         "Madrakhimova Zilolaxon",
    #         "Qoraqulov Akbarali",
    #         "A'zamov Abdulla",
    #         "Ashurov Ravshan",
    #         "Zikirov Obidjon",
    #         "Mamatqulov Musajon",
    #         "Sheraliev Shuhrat",
    #         "Bekniyazov Asan",
    #         "Rahmatov Nodirbek",
    #         "Koshanov Allanazar",
    #         "Qudaybergenov Allambergan",
    #         "Mutapoqulov X",
    #         "Sagdullaeva Maiz",
    #         "Lokaev Shuhrat"
    #     ],
    #     "Geometriya kafedrasi": [
    #         "Beshimov Ruzinazar",
    #         "Xadjiev Javvat",
    #         "Narmanov Abdigappar",
    #         "Mamatov Mashrabjon",
    #         "Sharipov Anvarjon",
    #         "Bayturaev Ashur",
    #         "Abdishukurova G.M.",
    #         "Aslonov Jhasurbek",
    #         "Saitova Sayyora",
    #         "Mukhamadiev Farhod",
    #         "Mamadaliev Nodirbek",
    #         "Safarova Dilnora",
    #         "Meyliev Shahboz",
    #         "Jo'rayev Rustam",
    #         "Diyarov Bexzod",
    #         "Ergashova Shohida",
    #         "Norqoziyev N.N.",
    #         "Zoidov A'zam",
    #         "Ruziev Jhalol",
    #         "Rajabov Eldor"
    #     ],
    #     "Ehtimollar nazariyasi kafedrasi": [
    #         "Sharipov Olimjon",
    #         "Formanov Shokir",
    #         "Muhammedov Abdurahmon",
    #         "Hamdamov Isakzhan",
    #         "Begmatov Abdumajid",
    #         "Xudoyqulova Xurriyat",
    #         "Rozieva Dilnura",
    #         "Kushmuradov Akmal",
    #         "Jalilov Akhtam",
    #         "Mukhtorov Ibrahim",
    #         "Hamdamov Ahad",
    #         "Halilova Gulhayo",
    #         "Hamidov Mukhritdin",
    #         "Sirojiddinov Abdulxamid",
    #         "Lazareva Viktoriya",
    #         "Husanboev Yo'qubjon",
    #         "Raimova Gulnora",
    #         "Azimov Jahongir",
    #         "Poshahodjaev",
    #         "Raimova Gulnora",
    #         "Qobilov O'tkir"
    #     ],
    #     "Mekhanika kafedrasi": [
    #         "Ahmedov Akrom",
    #         "Korshunova Natalya Aleksandrovna",
    #         "Begmatov Abduvali",
    #         "Xaldzhigitov Abduvali",
    #         "Zokirov Askar",
    #         "Mamatova Nigora",
    #         "Ibodulloyev Sherzod",
    #         "Ruzmatov Maksud",
    #         "Ahmedov Azamat",
    #         "Nazarov Farrukh",
    #         "Xolmonov Nurbek"
    #     ]
    # }
    # create_teacher(math_teachers)
    
    # others_teachers = {
    #     "O’zbekistonning eng yangi tarixi kafedrasi": [
    #         "Karimjonov Jasurbek",
    #         "Topildieva Muyassar",
    #         "Xayrullayeva Maftuna",
    #         "Polvanov Jaloliddin",
    #         "Raimova Aygul"
    #     ],
    #     "Ingliz tili kafedrasi": [
    #         "Eshboyeva Shoira",
    #         "Tursunova Sohiba",
    #         "Xoliqova Nazokat",
    #         "Jurayeva Gulxayo",
    #         "Lolayeva Zarima",
    #         "Irsaliyeva Madinaxon",
    #         "Xidirova Zuxra",
    #         "Suyunova Maftuna"
    #     ],
    #     "Rus tili kafedrasi": [
    #         "Shakarova Feruza",
    #         "Ten Svetlana",
    #         "Isakova Ravshana",
    #         "Yadgarova Guzal",
    #         "Akhmedova Muqaddas",
    #         "Raximova Alla"
    #     ],
    #     "Jismoniy tarbiya kafedrasi": [
    #         "Platunov Andrey"
    #     ],
    #     "O’zbek tili kafedrasi": [
    #         "Qurbonova Mushtariy"
    #     ],
    #     "Umumiy fizika kafedrasi": [
    #         "Raximova Yayra",
    #         "Turgunbayev Farxad",
    #         "Alimov Ravshan",
    #         "Saitqulov Dostonjon",
    #         "Tursunov Ikromjon",
    #         "Xolboyev Yunusali",
    #         "Kamilov Sherzad",
    #         "Sodiqova Shoxida"
    #     ],
    #     "Amaliy matematika kafedrasi": [
    #         "Xaydarov Abdugappar",
    #         "Saidov Doniyor",
    #         "Xojiyev Toji"
    #     ],
    #     "Dasturlash asoslari kafedrasi": [
    #         "Karimov Nodirbek",
    #         "Ikramov Axmat"
    #     ],
    #     "Olimova Muxlisa kafedrasi": [
    #         "Toshpo'Latov Abduhalil",
    #         "Abdujabbarov Zafar",
    #         "Polatov Asxad",
    #         "Adambayev Uchqunbek",
    #         "Falsafa",
    #         "Abdullayeva Nasiba",
    #         "Mengliqulov Umid",
    #         "Djalilov Baxtiyor",
    #         "Xidirov Mustafo",
    #         "Tyukmayeva Aida",
    #         "Qodirov Javlonbek"
    #     ],
    #     "Umumiy peagogika va psixologiya kafedrasi": [
    #         "Sodikov Ulugbek",
    #         "Shodmonov Shohruh",
    #         "Tulishov G'Olib",
    #         "Usmanova Shoira",
    #         "Murodov Mashrab",
    #         "Nig'Matova Shohsanam",
    #         "Xasanova Nozimaxon",
    #         "Xabiyev Temur"
    #     ],
    #     "Yosh fizoiologiyasi va geginya kafedrasi": [
    #         "Axmedova Saidaxon",
    #         "Mamatova Zulayxo",
    #         "Adilbekov Taxir",
    #         "Qayumov Hasan",
    #         "Patxullayeva Zilola",
    #         "Karimova Irodaxon",
    #         "Shukurova Diyora",
    #         "Komilov Esoxon",
    #         "Achilov Rashidbek",
    #         "Kasimov Nadim",
    #         "Dadajonov Rozmat"
    #     ]
    # }
    # create_teacher(others_teachers)


    # questions = ['O‘qituvchining dars o‘tish qobiliyati mahorati', 'Talabalar bilan muloqot qilish madaniyati', 'O‘qituvchining darsga tayyorgarlik ko‘rib kirishi', 'O‘qituvchining dars jarayoniga jiddiy qarashi, darslarning o‘z vaqtida tashkillashtirilishi', 'O‘qituvchining talabani adolatli baxolashi', 'Mashg‘ulotning mavzu doirasida olib borilishi', 'Mavzuni auditoriyaga eshitilarli, qiziqarli, mazmunli darajada yetkazib berishi', 'Mavzuni hozirgi dolzarb masalalarga bog‘lab tushuntirishi', 'O‘qituvchining ta’magirlikka moyilligi']
    # create_question(questions)



    answers = {
        "O‘qituvchining dars o‘tish qobiliyati mahorati": ["Qoniqarli", "Qoniqarsiz"],
        "Talabalar bilan muloqot qilish madaniyati": ["Qoniqarli", "Qoniqarsiz"],
        "O‘qituvchining darsga tayyorgarlik ko‘rib kirishi": ["Qoniqarli", "Qoniqarsiz"],
        "O‘qituvchining dars jarayoniga jiddiy qarashi, darslarning o‘z vaqtida tashkillashtirilishi": ["Qoniqarli", "Qoniqarsiz"],
        "O‘qituvchining talabani adolatli baxolashi": ["Qoniqarli", "Qoniqarsiz"],
        "Mashg‘ulotning mavzu doirasida olib borilishi": ["Darsni mavzu doirasida olib boradi", "Ko‘p hollarda darsni mavzu doirasida olib bormaydi"],
        "Mavzuni auditoriyaga eshitilarli, qiziqarli, mazmunli darajada yetkazib berishi": ["Qoniqarli", "Qoniqarsiz"],
        "Mavzuni hozirgi dolzarb masalalarga bog‘lab tushuntirishi": ["Qoniqarli", "Qoniqarsiz"],
        "O‘qituvchining ta’magirlikka moyilligi": ["Ta’magirlikka moyil emas", "Ta’magirlikka moyi"]
    }

    # create_answer(answers)
    