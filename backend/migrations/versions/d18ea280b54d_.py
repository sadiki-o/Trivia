"""empty message

Revision ID: d18ea280b54d
Revises: 7ec16e3a97a1
Create Date: 2022-08-12 23:56:09.982038

"""

from alembic import op
from sqlalchemy import DDL, event


# revision identifiers, used by Alembic.
revision = 'd18ea280b54d'
down_revision = '7ec16e3a97a1'
branch_labels = None
depends_on = None



def upgrade():
    #code responsible for handling artists availability when creating a show
    conn = op.get_bind()
    availability_trigger = DDL('''
        insert into public.users (id, username, password, public_id, created_at) values
        (0, 'admin', 'sha256$84u6xjShWh31CoHc$a0d5abed22ee8668971f2f53bd6ee950e456bf9069ee2502e1819b2d82394052', 'dbe03fa7-b080-4ef4-8c81-30bdb330a4f1', now());
    
        insert into public.categories (id, type, ownership) values
        (1, 'Science', 0),
        (2, 'Art', 0),
        (3, 'Geography', 0),
        (4, 'History', 0),
        (5, 'Entertainment', 0),
        (6, 'Sports', 0);
        SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories));


        insert into public.questions (id, question, answer, difficulty, category, ownership) values
        (5,	'Whose autobiography is entitled ''I Know Why the Caged Bird Sings?', 'Maya Angelou', 2, 4, 0),
        (9,	'What boxer''s original name is Cassius Clay?', 'Muhammad Ali', 1, 4, 0),
        (2,	'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?', 'Apollo 13', 4, 5, 0),
        (4,	'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?', 'Tom Cruise', 4, 5, 0),
        (6,	'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?', 'Edward Scissorhands', 3, 5, 0),
        (10, 'Which is the only team to play in every soccer World Cup tournament?', 'Brazil', 3, 6, 0),
        (11, 'Which country won the first ever soccer World Cup in 1930?', 'Uruguay', 4, 6, 0),
        (12, 'Who invented Peanut Butter?', 'George Washington Carver', 2, 4, 0),
        (13, 'What is the largest lake in Africa?', 'Lake Victoria', 2, 3, 0),
        (14, 'In which royal palace would you find the Hall of Mirrors?', 'The Palace of Versailles', 3, 3, 0),
        (15, 'The Taj Mahal is located in which Indian city?', 'Agra', 2, 3, 0),
        (16, 'Which Dutch graphic artist-initials M C was a creator of optical illusions?', 'Escher', 1, 2, 0),
        (17, 'La Giaconda is better known as what?', 'Mona Lisa', 3, 2, 0),
        (18, 'How many paintings did Van Gogh sell in his lifetime?', 'One', 4, 2, 0),
        (19, 'Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?', 'Jackson Pollock', 2, 2, 0),
        (20, 'What is the heaviest organ in the human body?', 'The Liver', 4, 1, 0),
        (21, 'Who discovered penicillin?', 'Alexander Fleming', 3, 1, 0),
        (22, 'Hematology is a branch of medicine involving the study of what?', 'Blood', 4, 1, 0),
        (23, 'Which dung beetle was worshipped by the ancient Egyptians?', 'Scarab', 4, 4, 0),
        (24, 'What was the name of the first artificial Earth satellite?', 'Sputnik 1', 3, 1, 0),
        (25, 'How many objects are equivalent to one mole?', '6.022 x 10^23', 5, 1, 0),
        (26, 'Painter Piet Mondrian (1872 - 1944) was a part of what movement?', 'Neoplasticism', 3, 2, 0),
        (27, 'What is the capital of Denmark?', 'Copenhagen', 2, 3, 0),
        (28, 'Alaska is the largest state in the United States, true or false?', 'true', 2, 3, 0),
        (29, 'What is the last name of Edward and Alphonse in the Fullmetal Alchemist series?', 'Elric', 3, 4, 0),
        (30, 'Who played the sun baby in the original run of Teletubbies?', 'Jessica Smith', 4, 5, 0),
        (31, 'In season one of the US Kitchen Nightmares, Gordan Ramsay tried to save 10 different restaurants. How many ended up closing afterwards?', '9', 3, 5, 0),
        (32, 'Which team won the 2015-16 English Premier League?', 'Leicester City', 4, 6, 0),
        (33, 'Rocket League is a game which features..?', 'cars', 4, 6, 0),
        (34, 'Which European capital city gives its name to a 1981 song by Ultravox?', 'Vienna', 3, 6, 0),
        (35, 'What disease did sailors use to contract because of lack of Vitamin C?', 'Scurvy', 4, 1, 0)
        ;

        SELECT setval('questions_id_seq', (SELECT MAX(id) FROM questions));
        ''')
    op.get_bind()
    conn.execute(availability_trigger)



def downgrade():
    pass



