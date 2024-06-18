import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PIL import Image
import os

class ImageToPDFConverter:
    def __init__(self,root):
        self.root=root
        self.image_path=[] #where images are stored
        self.output_pdf_name = tk.StringVar() #the pdf name is stored
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.initialize_ui() #the app

    def initialize_ui(self):
        #TITLE
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Hevetica", 16, "bold")) #title
        title_label.pack(pady=10) #pack all title descriptions

        #SELECT IMGS BUTTON
        select_images_button = tk.Button(self.root, text="Select Images", command = self.select_images) #command uses the function in the button call
        select_images_button.pack(pady=(0, 10)) #pack all button descriptions

        #LIST BOX OF IMAGES TO BE CONVERTED
        self.selected_images_listbox.pack(pady=(0,10), fill=tk.BOTH, expand=True)

        #ENTER NAME TEXT
        label = tk.Label(self.root, text="Enter output PDF name: ")
        label.pack()

        #TEXTBOX FOR NAME
        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width = 40, justify = 'center') #text variable hold the name
        pdf_name_entry.pack()

        #CONVERT BUTTON
        convert_button = tk.Button(self.root, text="Convert to PDF", command = self.convert_images_to_pdf) #command uses the function in the button call
        convert_button.pack(pady=(20, 40)) #pack all button descriptions

#TWO FUNCTIONS ARE FOR SELECT IMAGES
    def select_images(self):
        #if click, open file explorere and open images
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]) #goes to file exp. and asks to open
            #file types = the types of files we will accept and * represents the name of the file
        #Now we have to store names of images
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        #if at start there are names --> clear and then store new ones
        self.selected_images_listbox.delete(0, tk.END)

        #store new names
        for image_path in self.image_paths:
            _, image_path = os.path.split(image_path) #takes away path like (/Downloads/cs) from presented list
            self.selected_images_listbox.insert(tk.END, image_path) #then store

#CONVERTING
    def convert_images_to_pdf(self):
        #check if user gave name --> if not assign random name to pdf
        if not self.image_paths:
            return 
        
        output_pdf_path = self.output_pdf_name.get() +".pdf" if self.output_pdf_name.get() else "output.pdf"

        pdf = canvas.Canvas(output_pdf_path, pagesize = (612, 792))

        #Now have to store in one pdf
        for image_path in self.image_paths:
            img = Image.open(image_path) #open images from image path
            #place images in center of page
            available_width=540
            available_height=720
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = img.width*scale_factor
            new_height=img.height*scale_factor
            #new values are values to help us put img in center of pdf page
            x = 612-new_width
            y = 792-new_height
            x_centered = x/2
            y_centered = y/2

            #margin and put img in pdf
            pdf.setFillColorRGB(255,255,255)
            pdf.rect(0,0, 612, 792, fill=True)
            pdf.drawInlineImage(img, x_centered, y_centered, width = new_width, height = new_height)
            pdf.showPage()

        pdf.save()



def main():
    root=tk.Tk()
    root.title("Image to PDF") #window title
    converter = ImageToPDFConverter(root)
    root.geometry("400x600") #dimensions of window
    
    root.mainloop() #everything needs to before this
    


if __name__=="__main__":
    main()
