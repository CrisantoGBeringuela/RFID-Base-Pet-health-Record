def pet_uploadImage():
    global selected_binary_data
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        with open(file_path, 'rb') as f:
            selected_binary_data = f.read()
            # mycursor.execute("INSERT INTO tb_picture (tb_PetImage) values (%s) ", (binary_data,))
            # con.commit()

            img = Image.open(file_path)
            img = img.resize((248, 248))
            img_tk = CTkImage(light_image=img, size=(248, 248))

            label = CTkLabel(petpictureFrame, image=img_tk, text="")
            label.image = img_tk
            label.place(x=3, y=3)


