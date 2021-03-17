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

#movie list shown in dropdown menu
movie_list=[]
for i in range(0,len(user_ratings.columns)):
   movie_list.append(user_ratings.columns[i])


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
root.geometry('800x900')

# create rappers to manage the gui
warpper1 = LabelFrame(root, text="Movies Watched")
warpper2 = LabelFrame(root, text="Movies Suggested")
warpper1.pack(padx=30, pady=40, fill="both", expand="yes")
warpper2.pack(padx=30, pady=40, fill="both", expand="yes")

# drop down box with thier label
Label(warpper1, text="Select 3 movies you watched and rate them").grid(row=0, column=0, padx=10, pady=10)
e1=Entry(warpper1,width=32)
e1.grid(row=2, column=0,)
e2=Entry(warpper1,width=32)
e2.grid(row=4, column=0, )
e3=Entry(warpper1,width=32)
e3.grid(row=6, column=0, )

# dropdown menu 1
moviecombo = ttk.Combobox(warpper1, value=movie_list,width=30)
ratingcombo = ttk.Combobox(warpper1, value=[1, 2, 3, 4, 5])
# dropdown menu 2
moviecombo2 = ttk.Combobox(warpper1, value=movie_list,width=30)
ratingcombo2 = ttk.Combobox(warpper1, value=[1, 2, 3, 4, 5])
# dropdown menu 1
moviecombo3 = ttk.Combobox(warpper1, value=movie_list,width=30)
ratingcombo3 = ttk.Combobox(warpper1, value=[1, 2, 3, 4, 5])

# button function to add selected movies
fake_user=[]
def addmovie(event):
        e1.insert(END,moviecombo.get())
        mov = [moviecombo.get(), int(ratingcombo.get())]
        fake_user.append(mov)
def addmovie2(event):
        e2.insert(END, moviecombo2.get())
        mov = [moviecombo2.get(), int(ratingcombo2.get())]
        fake_user.append(mov)
def addmovie3(event):
        e3.insert(END, moviecombo3.get())
        mov = [moviecombo3.get(), int(ratingcombo3.get())]
        fake_user.append(mov)

# comboSelect bind 1
ratingcombo.current(0)
ratingcombo.bind("<<ComboboxSelected>>", addmovie)
ratingcombo.grid(row=1, column=3, padx=10, pady=10)
moviecombo.current(0)
moviecombo.grid(row=1, column=0, padx=10, pady=10)
# comboSelect bind 2
ratingcombo2.bind("<<ComboboxSelected>>", addmovie2)
ratingcombo2.grid(row=3, column=3, padx=10, pady=10)
moviecombo2.grid(row=3, column=0, padx=10, pady=10)
# comboSelect bind 3
ratingcombo3.bind("<<ComboboxSelected>>", addmovie3)
ratingcombo3.grid(row=5, column=3, padx=10, pady=10)
moviecombo3.grid(row=5, column=0, padx=10, pady=10)

##show the movie recommanded with their ratings
result =Listbox(warpper2,width=40)
result.grid(row=2,column=1,)

#create error message when movies not selected
error_message=Label(warpper1, fg="red")
error_message.grid(row=8, column=0, )

# button to suggest movie
def calculate():
    # collecting similar movies so we can show the result
    if not  any((e1.get(),e2.get(),e3.get())) :
        error_message['text']="please enter at least one movie !"
    else:
      error_message.config(text="                         ")
      similar_movies = pd.DataFrame()
      for movie, rating in fake_user:
        similar_movies = similar_movies.append(get_similar(movie, rating), ignore_index=True)
    # printing the top 20 recommended movie
      s=similar_movies.sum().sort_values(ascending=False)
      i=0
      j=1
      for  i  in range(20):
       result.insert(END,s.iloc[i:j].to_string())
       j=j+1

# clear button fonction
def clear():
    fake_user.clear()
    moviecombo2.delete(0, END)
    ratingcombo2.delete(0, END)
    moviecombo3.delete(0, END)
    ratingcombo3.delete(0, END)
    e1.delete(0,END)
    e2.delete(0, END)
    e3.delete(0, END)
    result.delete(0,END)
    error_message.config(text="                           ")

#create buttons
B1 = Button(warpper1, text="Add Your Movie",padx=10, pady=10,borderwidth=2, command=calculate).grid(row=8, column=2, )
B2=  Button(warpper1, text="     clear    ", padx=24, pady=10,borderwidth=2,command=clear).grid(row=7, column=2, )

# list result in a list box
Label(warpper2,text=" ").grid(row=0,column=0)
Label(warpper2,text="                                                 ").grid(row=2,column=0)


root.resizable(width=False,height=True)
root.mainloop()