import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
from lin import train_test_split
from lin import LinearRegression
from log_multinom import LogisticRegression
from scaler import StandardScaler
import matplotlib.pyplot as plt
from log_bin import OneVsOneLogisticRegression
import threading

def validate_input(new_value):
    if new_value == '' or new_value.isdigit():
        return True
    else:
        return False
    
def load_subcategory(new_value):
    if new_value in cat_dict.keys():
        values = cat_dict[new_value]
        values.sort()
        subcategory_dropdown.configure(state='readonly', values=cat_dict[new_value])
        selected_subcategory.set('')
    else:
        return False
    
def submit():
    d = {}
    binding_type = -1
    main_category = ''
    subcategory = ''
    area = -1.0
    description_length = -1
    price = -1
    for entry in entries:
        if entries.index(entry) == labels.index('Year'):
            try:
                _ = int(entry.get())
            except:
                messagebox.showerror('Error', 'Year must be a number')
                return
            
        elif entries.index(entry) == labels.index('Title'):
            pass
        elif entries.index(entry) == labels.index('Author'):
            pass
        elif entries.index(entry) == labels.index('Pages'):
            pages = int(entry.get())
        elif entries.index(entry) == labels.index('Binding'):
            binding_type = int(entry.get())
        elif entries.index(entry) == labels.index('Format'):
            try:
                l = entry.get().split('x')
                if len(l) != 2:
                    raise Exception
                else:
                    l1 = float(l[0])
                    l2 = float(l[1])
            except:
                try:
                    l = entry.get().split('*')
                    if len(l) != 2:
                        raise Exception
                    else:
                        l1 = float(l[0])
                        l2 = float(l[1])
                except:
                    messagebox.showerror('Error', 'Format must be NUMxNUM or NUM*NUM')
                    return
            area = pages * l1 * l2
        elif entries.index(entry) == labels.index('Description'):
            description_length = len(entry.get('1.0', 'end').strip())
            continue
        elif entries.index(entry) == labels.index('Category'):
            main_category = ''
            for key, value in categories_dict.items():
                if value == entry.get():
                    main_category = key
                    break
            main_category = int(main_category)
        elif entries.index(entry) == labels.index('Subcategory'):
            subcategory = ''
            for key, value in subcategories_dict.items():
                if value == entry.get():
                    subcategory = key
                    break
            if subcategory == '':
                subcategory = 0
            subcategory = int(subcategory)
        if entry.get() == '':
            messagebox.showerror('Error', 'Input all fields')
            return
    d['binding_type'] = binding_type
    d['main_category'] = main_category
    d['subcategory'] = subcategory
    d['area'] = area
    # d['description_length'] = description_length
    # d['price'] = 0
    if int(entries[-1].get()) == 2:
        d['price'] = 0
        df = pd.DataFrame(d, index=[0])
        new_data_frame = pd.DataFrame(scaler_lin.transform(df), columns=df.columns, index=df.index)
        new_data_frame.drop('price', axis=1, inplace=True)
        predictions = lin.predict(new_data_frame)

        y_t = pd.DataFrame(predictions, columns=['price'])
        result = pd.concat([new_data_frame.reset_index(drop=True), y_t], axis=1)

        predictions_unscaled = scaler_lin.inverse_transform(result)

        predictions_df = pd.DataFrame(predictions_unscaled, columns=result.columns)

        predictions_df['price'] = predictions_df['price'].apply(lambda x: '{:.2f}'.format(x))
        if checkbox_var.get() == 'on':
            plot_lin(predictions_df.iloc[0])
        final_label.configure(text='Result: ' +  predictions_df.iloc[0]['price'])
    else:    
        d['price_range'] = 0
        df = pd.DataFrame(d, index=[0])
        new_data_frame = pd.DataFrame(scaler.transform(df), columns=df.columns, index=df.index)
        # new_data_frame = df
        new_data_frame.drop('price_range', axis=1, inplace=True)
        if int(entries[-1].get()) == 0:
            predictions = log_bin.predict(new_data_frame)
        else:
            predictions = log_multinom.predict(new_data_frame)

        y_t = pd.DataFrame(predictions, columns=['price_range'])
        result = pd.concat([new_data_frame.reset_index(drop=True), y_t], axis=1)

        predictions_unscaled = scaler.inverse_transform(result)

        predictions_df = pd.DataFrame(predictions_unscaled, columns=result.columns)
        # predictions_df = pd.DataFrame(result, columns=result.columns)

        predictions_df['price_range'] = predictions_df['price_range'].apply(lambda x: '{:.2f}'.format(x))
        res_index = price_labels.index(int(float(predictions_df.iloc[0]['price_range'])))
        if checkbox_var.get() == 'on':
            plot_log(predictions_df.iloc[0])
        final_label.configure(text='Result: ' +  price_labels_range[res_index])
           
def plot_log(dot):
    data_to_plot = data_log
    df_mapped = data_to_plot['main_category'].map(categories_dict)
    data_to_plot['category'] = df_mapped
    dot['category'] = categories_dict[int(dot['main_category'])]
    data_to_plot = data_to_plot.drop(['subcategory'], axis=1)
    dot = dot.drop(['subcategory'])
    dot['price_range'] = float(dot['price_range'])

    marker_dict = {
        1: ('s', 'Tvrd'),
        0: ('^', 'Broš')
    }

    plt.figure(figsize=(15, 8))
    for value, (marker, label) in marker_dict.items():
        subset = data_to_plot[data_to_plot['binding_type'] == value]
        subset['price_range'] = subset['price_range'].astype(float)
        scatter = plt.scatter(subset['category'], subset['area'], c=subset['price_range'], cmap='viridis', s=20, alpha=0.75, marker=marker, label=label)

    plt.scatter(dot['category'], dot['area'], s=30, color='red', marker='o')
    cbar = plt.colorbar(scatter)
    cbar.set_label('Cena')

    plt.rcParams.update({'font.size': 14})
    plt.xlabel('Kategorija')
    plt.ylabel('Broj stranica x Format')
    plt.subplots_adjust(bottom=0.35)
    plt.title('Grafik')
    plt.xticks(rotation=45)
    plt.rcParams.update({'font.size': 14})
    plt.legend(title='Povez')

    plt.show()   
    
def plot_lin(dot):
    data_to_plot = data_lin
    df_mapped = data_to_plot['main_category'].map(categories_dict)
    data_to_plot['category'] = df_mapped
    dot['category'] = categories_dict[int(dot['main_category'])]
    data_to_plot = data_to_plot.drop(['subcategory'], axis=1)
    dot = dot.drop(['subcategory'])

    marker_dict = {
        1: ('s', 'Tvrd'),
        0: ('^', 'Broš')
    }

    plt.figure(figsize=(15, 8))
    for value, (marker, label) in marker_dict.items():
        subset = data_to_plot[data_to_plot['binding_type'] == value]
        subset['price'] = subset['price'].astype(float)
        scatter = plt.scatter(subset['category'], subset['price'].astype(float), c=subset['area'], cmap='viridis', s=20, alpha=0.75, marker=marker, label=label)

    dot['price'] = float(dot['price'])
    plt.scatter(dot['category'], dot['price'], s=30, color='red', marker='o')
    cbar = plt.colorbar(scatter)
    cbar.set_label('Broj stranica x Format')

    plt.rcParams.update({'font.size': 14})
    plt.xlabel('Kategorija', fontsize=14)
    plt.ylabel('Cena', fontsize=14)
    plt.subplots_adjust(bottom=0.35)
    plt.title('Grafik')
    plt.xticks(rotation=45)
    plt.legend(title='Povez')

    plt.show()

  
def background_task():
    log_multinom.fit(X_train_log, y_train_log, class_labels=scaled_labels)
    log_bin.fit(X_train_log,y_train_log)
    lin.fit(X_train, y_train)

    submit_button.configure(state='normal')
    
# model fitting
data = pd.read_json('books_pre.json')
col = data.pop('price')
data['price'] = col
price_ranges = [(0, 500), (500, 1500), (1500, 3000), (3000, 5000), (5000, 10000), (10000, 15000), (15000, float('inf'))]
price_labels = [0, 500, 1500, 3000, 5000, 10000, 15000]
price_labels_range = ['< 500', '500-1500', '1500-3000', '3000-5000', '5000-10000', '10000-15000', '> 15000']

data_lin = data.copy()
data_log = data.copy()
scaler_lin = StandardScaler()
new_df = pd.DataFrame(scaler_lin.fit_transform(data_lin), columns=data_lin.columns, index=data_lin.index)
X = new_df.drop('price', axis=1)
y = new_df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0)

data_log['price_range'] = pd.cut(data_log['price'], bins=[x[0] for x in price_ranges] + [float('inf')], labels=price_labels, right=False)
scaler = StandardScaler()
data_log.drop(['price'], axis=1, inplace=True)
data_log['price_range'] = data_log['price_range'].astype(float)
new_df = pd.DataFrame(scaler.fit_transform(data_log), columns=data_log.columns, index=data_log.index)
scaled_labels = new_df['price_range'].unique()
scaled_labels.sort()
X_log = new_df.drop(['price_range'], axis=1)
y_log = new_df['price_range']

X_train_log, X_test_log, y_train_log, y_test_log = train_test_split(X_log, y_log, random_state=42, test_size=0)

categories = pd.read_json('category_mapping.json')
subcategories = pd.read_json('category2_mapping.json')
cat = pd.read_json('categories.json')
cat.drop_duplicates(inplace=True)

categories_dict = {}
subcategories_dict = {}
cat_dict = {}

for item in categories.values:
    categories_dict[item[1]] = item[0]

for item in subcategories.values:
    subcategories_dict[item[1]] = item[0]

for item in cat.values:
    if item[0] not in cat_dict.keys():
        cat_dict[item[0]] = []
    cat_dict[item[0]].append(item[1])

lin = LinearRegression(lr=0.01, num_iterations=10000)
log_multinom = LogisticRegression(lr=0.1, num_iterations=3000)
log_bin = OneVsOneLogisticRegression()

# app window

def change_theme_event(new_theme: str):
    ctk.set_appearance_mode(new_theme)
    
ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('green')
root = ctk.CTk()
root.title('Book Price Prediction')
root.resizable(False, False)
root.geometry('450x650')

frame_options = ctk.CTkFrame(root, height=50, corner_radius=0)
frame_options.pack(fill='both')
frame_options.grid_columnconfigure(1, weight=1)
frame_options.grid_columnconfigure(2, weight=1)
frame_options.grid_columnconfigure(3, weight=1)
theme_label = ctk.CTkLabel(frame_options, text='Theme:', anchor='w', justify='left')
theme_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky='NSEW')
theme_optionmenu = ctk.CTkOptionMenu(frame_options, values=['Dark', 'Light', 'System'], command=change_theme_event)
theme_optionmenu.grid(row=1, column=1, padx=20, pady=(10, 10), sticky='NSEW')

label = ctk.CTkLabel(frame_options, text='Type:')
label.grid(row=2, column=0, padx=5, pady=5)
type_radio = ctk.StringVar()
entry_multinom = ctk.CTkRadioButton(frame_options, text='Log Multinomial', variable=type_radio, value='1')
entry_multinom.grid(row=2, column=1, padx=5, pady=5, sticky='NSEW')
entry_bin = ctk.CTkRadioButton(frame_options, text='Log OVO', variable=type_radio, value='0')
entry_bin.grid(row=2, column=2, padx=5, pady=5, sticky='NSEW')
entry_linear = ctk.CTkRadioButton(frame_options, text='Linear', variable=type_radio, value='2')
entry_linear.grid(row=2, column=3, padx=5, pady=5, sticky='NSEW')

frame = ctk.CTkFrame(root)
frame.pack(padx=10, pady=10, fill='both', expand=True, anchor='w')
frame.grid_rowconfigure(10, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)

big_font = ctk.CTkFont(size=24, weight='bold')

entries = []

labels = ['Title', 'Author', 'Publisher', 'Year', 'Pages', 'Binding', 'Format', 'Category', 'Subcategory', 'Description']

for i in range(len(labels)):
    label = ctk.CTkLabel(frame, text=labels[i]+':')
    label.grid(row=i+1, column=0, padx=5, pady=5, sticky='NSEW')
    if labels[i] == 'Binding':
        selected_radio = ctk.StringVar()
        entry1 = ctk.CTkRadioButton(frame, text='Hardcover', variable=selected_radio, value='3')
        entry1.grid(row=i+1, column=1, padx=5, pady=5, sticky='NSEW')
        entry2 = ctk.CTkRadioButton(frame, text='Paperback', variable=selected_radio, value='0')
        entry2.grid(row=i+1, column=2, padx=5, pady=5, sticky='NSEW')
        entries.append(selected_radio)
    elif labels[i] == 'Year':
        year_options = [str(year) for year in range(2024, 1900, -1)]
        selected_year = ctk.StringVar()
        selected_year.set(year_options[0])
        year_dropdown = ctk.CTkComboBox(frame, variable=selected_year, values=year_options)
        year_dropdown.grid(row=i+1, column=1, padx=5, pady=5, columnspan=2, sticky='NSEW')
        entries.append(year_dropdown)
    elif labels[i] == 'Pages':
        validate_numeric = root.register(validate_input)
        entry = ctk.CTkEntry(frame, validate='key', validatecommand=(validate_numeric, '%P'))
        entry.grid(row=i+1, column=1, padx=5, pady=5, columnspan=2, sticky='NSEW')
        entries.append(entry)
    elif labels[i] == 'Category':
        category_options = list(categories_dict.values())
        category_options.sort()
        selected_category = ctk.StringVar()
        selected_category.set('')
        category_dropdown = ctk.CTkComboBox(frame, variable=selected_category, values=category_options, state='readonly', command=load_subcategory)
        category_dropdown.grid(row=i+1, column=1, padx=5, pady=5, columnspan=2, sticky='NSEW')
        entries.append(category_dropdown)
    elif labels[i] == 'Subcategory':
        subcategory_options = list(subcategories_dict.values())
        subcategory_options.sort()
        selected_subcategory = ctk.StringVar()
        selected_subcategory.set('')
        subcategory_dropdown = ctk.CTkComboBox(frame, variable=selected_subcategory, values=subcategory_options, state='readonly')
        subcategory_dropdown.grid(row=i+1, column=1, padx=5, pady=5, columnspan=2, sticky='NSEW')
        subcategory_dropdown.configure(state='disabled')
        entries.append(subcategory_dropdown)
    elif labels[i] == 'Description':
        entry = ctk.CTkTextbox(frame, wrap='word', height=50)
        entry.grid(row=i+1, column=1, padx=5, pady=5, columnspan=2, sticky='NSEW')
        entries.append(entry)
    else:
        entry = ctk.CTkEntry(frame)
        entry.grid(row=i+1, column=1, padx=5, pady=5, columnspan=2, sticky='NSEW')
        entries.append(entry)

entries.append(type_radio)

checkbox_var = ctk.StringVar()
checkbox_var.set('off')
checkbox = ctk.CTkCheckBox(root, text='Plot', variable=checkbox_var, onvalue='on', offvalue='off')
checkbox.pack(padx=10)
    
final_label = ctk.CTkLabel(root, text='Result:', font=big_font)
final_label.pack(pady=20)

submit_button = ctk.CTkButton(root, text='Submit', command=submit, state='disabled')
submit_button.pack(pady=10)

thread = threading.Thread(target=background_task, daemon=True)
thread.start()

root.mainloop()
