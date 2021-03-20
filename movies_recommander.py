from tkinter import ttk
from tkinter import *
import pandas as pd


# ####################################################################################################################
# #                                           backend                                                               ##
# ####################################################################################################################
# # movie lens data set import
ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')



# # merging the two files to get the movies and ratings in one file + dropping unwanted columns
ratings = pd.merge(movies, ratings).drop(['genres', 'timestamp'], axis=1)

# # changing the data structure to ease the work
user_ratings = ratings.pivot_table(index=['userId'], columns=['title'], values='rating')

# # remove movies who were rated by lesser than 10 user and fill Nan with 0
user_ratings = user_ratings.dropna(thresh=10, axis=1).fillna(0)

# # applying the pearson methode to get the similarities between the movies
item_similarity_df = user_ratings.corr(method='pearson')

def get_similar(movie_name, rating):
# # get the similarity score and subtracting 2.5 from the rating to fix placement of bad movies in the list
  similar_score = item_similarity_df[movie_name]*(rating-2.5)
  similar_score = similar_score.sort_values(ascending=False)
  return similar_score

################################################################################################################
#                                                  GUI CODE                                                    #
#################################################################################################################"
root = Tk()
root.title("Master 2 IAM")
root.configure(bg='#4b5162')
root.geometry('960x900')

# creatwrappers to manage the gui
wrapper1 = Frame(root, bg='#383c4a')
wrapper2 = Frame(root, bg='#4b5162')
wrapper3 = Frame(root, bg='#4b5162')
wrapper1.pack(padx=0, pady=0, fill="both")
wrapper2.pack(padx=30, pady=40, fill="both", expand="yes")
wrapper3.pack(padx=30, pady=40, fill="both", expand="yes")

# header

Label(wrapper1, text="MOVIE RECOMMENDER", bg='#383c4a', fg='white', font=("Chango", 33)).pack(pady=10)
# drop down box with their label
Label(wrapper2, text="Select 3 movies you watched and rate them", fg='white', bg='#4b5162').grid(row=0, column=2, padx=10, pady=10)
e1 = Entry(wrapper2, width=32, fg='white', bg='#4b5162')
e1.grid(row=2, column=2)
e2 = Entry(wrapper2, width=32, fg='white', bg='#4b5162')
e2.grid(row=4, column=2)
e3 = Entry(wrapper2, width=32, fg='white', bg='#4b5162')
e3.grid(row=6, column=2)

#movie list shown in dropdown menu
movie_list=[]
for i in range(0,len(user_ratings.columns)):
   movie_list.append(user_ratings.columns[i])

# dropdown menu 1
movie_combo = ttk.Combobox(wrapper2, value=movie_list, width=32)
rating_combo = ttk.Combobox(wrapper2, value=[1, 2, 3, 4, 5], width=32)
# dropdown menu 2
movie_combo2 = ttk.Combobox(wrapper2, value=movie_list, width=32)
rating_combo2 = ttk.Combobox(wrapper2, value=[1, 2, 3, 4, 5], width=32)
# dropdown menu 1
movie_combo3 = ttk.Combobox(wrapper2, value=movie_list, width=32)
rating_combo3 = ttk.Combobox(wrapper2, value=[1, 2, 3, 4, 5], width=32)

# button function to add selected movies
fake_user = []


def add_movie(event):
    e1.delete(0,END)
    e1.insert(END, movie_combo.get())
    mov = [movie_combo.get(), int(rating_combo.get())]
    fake_user.append(mov)


def add_movie2(event):
    e2.delete(0, END)
    e2.insert(END, movie_combo2.get())
    mov = [movie_combo2.get(), int(rating_combo2.get())]
    fake_user.append(mov)


def add_movie3(event):
    e3.delete(0, END)
    e3.insert(END, movie_combo3.get())
    mov = [movie_combo3.get(), int(rating_combo3.get())]
    fake_user.append(mov)


# comboSelect bind 1
rating_combo.bind("<<ComboboxSelected>>", add_movie)
rating_combo.grid(row=1, column=3, padx=10, pady=10)
movie_combo.grid(row=1, column=0, padx=10, pady=10)
# comboSelect bind 2
rating_combo2.bind("<<ComboboxSelected>>", add_movie2)
rating_combo2.grid(row=3, column=3, padx=10, pady=10)
movie_combo2.grid(row=3, column=0, padx=10, pady=10)
# comboSelect bind 3
rating_combo3.bind("<<ComboboxSelected>>", add_movie3)
rating_combo3.grid(row=5, column=3, padx=10, pady=10)
movie_combo3.grid(row=5, column=0, padx=10, pady=10)

# show the movie recommended with their ratings
result = Listbox(wrapper3, width=40)
result.grid(padx=288, row=3, column=2)

# create error message when movies not selected
error_message = Label(wrapper2, fg="red", bg='#4b5162',font='bold')
error_message.grid(row=9, column=2, )


# button to suggest movie
def calculate():
    # collecting similar movies so we can show the result
    if not any((e1.get(), e2.get(), e3.get())):
        error_message['text'] = "please enter at least one movie !"
    else:
        error_message.config(text="                         ")
        similar_movies = pd.DataFrame()
        for movie, rating in fake_user:
            similar_movies = similar_movies.append(get_similar(movie, rating), ignore_index=True)
        # printing the top 20 recommended movie
        s = similar_movies.sum().sort_values(ascending=False)
        i = 0
        j = 1
        for i in range(20):
            result.insert(END, s.iloc[i:j].to_string())
            j = j + 1


# clear button function
def clear():
    fake_user.clear()
    movie_combo.delete(0, END)
    rating_combo.delete(0, END)
    movie_combo2.delete(0, END)
    rating_combo2.delete(0, END)
    movie_combo3.delete(0, END)
    rating_combo3.delete(0, END)
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    result.delete(0, END)
    error_message.config(text="                           ")


# create buttons
B1 = Button(wrapper2, text="Add Your Movie", bg='#7c818c', fg='white', padx=10, pady=10, borderwidth=2, command=calculate).grid(row=8, column=0)
B2 = Button(wrapper2, text="     clear    ", bg='#7c818c', fg='white', padx=24, pady=10, borderwidth=2, command=clear).grid(row=8, column=3)

# list result in a list box
Label(wrapper3, text="Our Recommendation", bg='#4b5162', fg='white').grid(row=0, column=2)

root.resizable(width=False,height=True)
root.mainloop()