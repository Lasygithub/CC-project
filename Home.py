import streamlit as st
import cv2
from PIL import Image
import pandas as pd
import re
import requests
import time

WEBHOOK_URL = "https://connect.pabbly.com/workflow/sendwebhookdata/IjU3NjUwNTY0MDYzMDA0MzY1MjY0NTUzNjUxMzci_pc"


        
#csv file
df = pd.read_csv('E:\cars1.csv')

#----------------------------------------------------side bar-----------------------------------------------------------
st.logo(
    "E:\lalo.png",
    icon_image="E:\smlo.png",
)
st.sidebar.title("CAR COMPASS")
page=st.sidebar.selectbox("CHOOSE A PAGE",["HOME","CHATBOT","ABOUT","PROFILE","CONTACT US/FEEDBACK"])
if page=="HOME":
    st.markdown(
        """
        <h1 style='text-align: center;'>CAR COMPASS</h1>
        """,
        unsafe_allow_html=True
    )


#-------------------------------------------------------------------input_name----------------------------------------------------------
    x = st.text_input("Enter your name:")
    sn = ['dipesh', 'DIPESH', 'Dipesh kumar', 'dipesh kumar', 'yogit', 'YOGIT', 'yg', 'yogit krishnan', 'YOGIT KRISHNAN', 'Yogit Krishnan']
    sn1 = ['joseph', 'joseph anand', 'Joseph Anand']
    
    if x in sn:
        st.write("Hi boss ")
    elif x in sn1:
        st.write("Vanakkam Vathiyaare")
    elif x:
        st.write("HI",x,"I am CC(CAR COMPASS) BOT")
        st.write("I am here to help you with finding appropriate cars for you ")
    st.divider()
#-----------------------------------------------------img1----------------------------------------------------------------------
    image_path = 'E:\cci.png'
    img = Image.open(image_path)
    st.image(img, width=700)
    st.divider()
#----------------------------------------------------input criterias---------------------------------------------------------------
    br = st.multiselect(
        "SELECT CAR BRAND(S)",
        df['brand'].unique(),
        placeholder="SELECT BRAND(S)..."
    )
    
    ca = st.multiselect(
        "SELECT CAR CATEGORY(IES)",
        df['category'].unique(),
        placeholder="SELECT CATEGORY(IES)..."
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    
    bu_min = st.number_input(
        "ENTER MINIMUM BUDGET (IN RUPEES)",
        min_value=int(df['price_rupees'].min()),
        max_value=int(df['price_rupees'].max()),
        step=100000,
        value=int(df['price_rupees'].min())
    )
    
    bu_max = st.number_input(
        "ENTER MAXIMUM BUDGET (IN RUPEES)",
        min_value=int(bu_min),
        max_value=int(df['price_rupees'].max()),
        step=1000000,
        value=int(df['price_rupees'].max())
    )
    
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    
    ns = st.selectbox(
        "SELECT NO. OF SEATS",
        sorted(df['no_of_seats'].unique()),
        index=sorted(df['no_of_seats'].unique()).index(5),
        placeholder="SELECT NO. OF SEATS..."
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    
    mi_min, mi_max = st.slider(
        "SELECT MILEAGE RANGE (IN KM/L)",
        min_value=int(df['mileage_km_per_l'].min()),
        max_value=int(df['mileage_km_per_l'].max()),
        value=(int(df['mileage_km_per_l'].min()), int(df['mileage_km_per_l'].max()))
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    
    filtered_df = df[
        df['brand'].isin(br) &
        df['category'].isin(ca) &
        (df['price_rupees'] >= bu_min) &
        (df['price_rupees'] <= bu_max) &
        (df['no_of_seats'] == ns) &
        (df['mileage_km_per_l'] >= mi_min) &
        (df['mileage_km_per_l'] <= mi_max)
    ]
    
    if not filtered_df.empty:
        st.write(f"Found {len(filtered_df)} car(s) matching your criteria:")
        for index, row in filtered_df.iterrows():
            st.markdown(f"### {row['car_name']}")
            st.image(row['file_path'], width=500)
            st.write(f"**Category**: {row['category']}")
            st.write(f"**Price**: {row['price_rupees']} INR")
            st.write(f"**Seats**: {row['no_of_seats']}")
            st.write(f"**Mileage**: {row['mileage_km_per_l']} km/l")
            st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.write("No cars found that match your criteria.")

#-----------------------------------------------chatbot-----------------------------------------------------------------------

elif page=="CHATBOT":
    faqs = {
    "Hi":"HI",
    "Hello":"hello",
    "What is your name":"CC(CAR COMPASS)CHATBOT",
    "Are you a human":"I am a chatbot",
    "Do you like cars":"yes I absoluetly like cars",
    "What is car compass?": "It is a web application used to help you find the right and appropriate car for your needs.",
    "Who are you?": "I am CC the chatbot designed to help you find the right car and clarify doubts about cars.",
    "Who founded Car Compass?": "Car Compass was founded by Mr. Dipesh Kumar and Mr. Yogit Krishnan.",
    "Who is Durai Murugan?": "Ivan dhaan gold eh",
    "What is a car?": "A car is a vehicle used for transportation that makes our lives more convenient.",
    "Who is Dipesh Kumar?": "He is one of the founders of Car Compass, but definitely less intelligent than me.",
    "Who is Yogit Krishnan?": "He is also a founder of Car Compass, and he's one of the most difficult people I’ve ever had to work with.",
    "What are some popular car brands in India?": "Some popular car brands include Toyota, Mahindra, BMW, Audi, and Maruti Suzuki.",
    "What is the best car for fuel efficiency?": "Cars like the Toyota Glanza, Maruti Celerio, and Maruti Suzuki Swift are known for their excellent fuel efficiency.",
    "How often should I service my car?": "It's recommended to service your car every 6 months or every 8,000 kilometres, whichever comes first.",
    "What is the average lifespan of a car?": "The average lifespan of a car is about 12 years or 300,000 kilometres, but this can vary depending on maintenance and usage.",
    "How can I improve my car's fuel efficiency?": "To improve fuel efficiency, keep your tires properly inflated, avoid excessive idling, maintain a steady speed, and remove unnecessary weight from your car.",
    "What are the benefits of electric cars?": "Electric cars are environmentally friendly, have lower running costs, require less maintenance, and often come with government incentives.",
    "What are hybrid cars?": "Hybrid cars combine a gasoline engine with an electric motor, offering better fuel efficiency and reduced emissions compared to traditional gasoline-only vehicles.",
    "How does car financing work?": "Car financing allows you to pay for a vehicle over time through monthly payments. This typically involves taking out a loan from a bank, credit union, or dealership.",
    "What should I do if my car's check engine light comes on?": "If your car's check engine light comes on, it's important to have it diagnosed as soon as possible. It could be a minor issue or something more serious, so don't ignore it.",
    "How can I extend the life of my car?": "Regular maintenance, such as oil changes, tire rotations, and brake inspections, is key to extending the life of your car. Driving gently and avoiding harsh conditions also helps.",
    "What are the advantages of leasing a car?": "Leasing a car typically offers lower monthly payments and allows you to drive a new car every few years. However, you don't own the car at the end of the lease term.",
    "What is the difference between all-wheel drive (AWD) and four-wheel drive (4WD)?": "AWD is typically used in cars and crossovers for better traction on slippery roads, while 4WD is designed for off-road and rugged terrain, providing power to all four wheels simultaneously.",
    "How do I choose the right tires for my car?": "Choosing the right tires depends on your driving conditions, climate, and the type of vehicle you have. Consider all-season tires for general use, winter tires for snow, and performance tires for enhanced handling.",
    "What are the signs that my car needs new brakes?": "Signs that your car needs new brakes include squeaking or grinding noises, a longer stopping distance, and a brake pedal that feels soft or spongy.",
    "How does a car's resale value get determined?": "A car's resale value is determined by factors like age, mileage, condition, brand reputation, and market demand. Regular maintenance and keeping the car in good condition help maintain its value.",
    "What are some tips for buying a new car?": "When buying a new car, research different models, compare prices, test drive multiple vehicles, and negotiate the price. It's also wise to consider financing options and read reviews.",
    "How can I reduce my car insurance costs?": "To reduce car insurance costs, consider increasing your deductible, bundling insurance policies, maintaining a clean driving record, and asking about discounts for safety features or low mileage.",
    "What should I do if my car overheats?": "If your car overheats, pull over safely, turn off the engine, and wait for it to cool down. Check the coolant level and look for leaks. It's best to have a mechanic inspect the car before driving again.",
    "How can I safely tow a trailer with my car?": "To safely tow a trailer, ensure your car is equipped with the proper towing package, distribute weight evenly, drive at moderate speeds, and use safety chains. Make sure to follow the vehicle's towing capacity guidelines.",
    "What is the difference between petrol and diesel cars?": "Petrol cars are generally quieter and offer a smoother drive, while diesel cars tend to have better fuel efficiency and more torque, making them suitable for longer drives.",
    "What is a turbocharged engine?": "A turbocharged engine uses a turbine to force extra air into the engine, increasing power without significantly increasing fuel consumption.",
    "How does an automatic transmission differ from a manual transmission?": "An automatic transmission shifts gears on its own, providing easier and more convenient driving, while a manual transmission requires the driver to shift gears using a clutch and gear stick.",
    "What is adaptive cruise control?": "Adaptive cruise control is a feature that automatically adjusts your car's speed to maintain a safe following distance from the vehicle ahead.",
    "What are the advantages of keyless entry?": "Keyless entry allows you to unlock and start your car without using a traditional key, offering added convenience and security.",
    "What is a car's drivetrain?": "A car's drivetrain refers to the system that delivers power from the engine to the wheels, including the transmission, driveshaft, and differential.",
    "What does the term 'horsepower' mean in a car?": "Horsepower is a unit of measurement for engine power, indicating how much work the engine can perform over time. Higher horsepower generally means better acceleration and speed.",
    "What is a car's suspension system?": "A car's suspension system is responsible for providing a smooth ride by absorbing shocks from the road and maintaining tire contact with the road surface.",
    "How do I maintain my car's battery?": "To maintain your car's battery, keep the terminals clean, ensure it's securely fastened, check the charge regularly, and avoid leaving lights or electronics on when the engine is off.",
    "What are run-flat tires?": "Run-flat tires are designed to be driven on even after a puncture, allowing you to continue driving for a short distance to reach a repair shop.",
    "What is a car's VIN?": "A Vehicle Identification Number (VIN) is a unique code assigned to every vehicle, providing information about its make, model, year, and manufacturing details."
}

    def get_faq_response(question):
        question = question.strip().lower()
        for q, a in faqs.items():
            if question in q.lower():
                return a
        return "I'm sorry, I don't have an answer for that question. Please try asking another question."

    st.title("Car Compass FAQ Chatbot")


    st.header("Ask a Car-Related Question")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your question here:"):
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        response = get_faq_response(prompt)

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


#------------------------------------------------about--------------------------------------------------------------------
elif page == "ABOUT":
    st.markdown(
        """
        <h1 style='text-align: center;'>ABOUT US</h1>
        """,
        unsafe_allow_html=True
    )

    image_path = 'E:\CC_3.png'
    img = Image.open(image_path)
    st.image(img, width=700)
    st.divider()

    multi='''This is car compass. This is the site where you will get to explore wide variety of cars,
             You can choose your dream car and get to know about it. 
             This site is under development and will be developed throughout the time.

             Created by school students.

             Car Compass beta version 2.0
          '''
    st.markdown(multi)



#---------------------------------------------------------portfolio-----------------------------------------------------

elif page == "PROFILE":
    st.markdown(
        """
        <h1 style='text-align: center;'>PROFILE</h1>
        """,
        unsafe_allow_html=True
    )
    st.write("This site's 'so-acclaimed founders' are Mr. Dipesh and Mr .YG Profile's are given below:")
    st.write("Programmer of Car Compass,Mr.Dipesh Kumar's Profile")
    st.link_button("DIPESH'S PROFILE", "https://lazydipesh.carrd.co/")
    st.write("Data analayst of Car Compass,Mr. Yogit Krishnan's Profile")
    st.link_button("YOGIT KRISHNAN'S PROFILE", "https://alwaysyg.carrd.co/")
    
#-----------------------------------------------------contact form ------------------------------------------------------------           
elif page =="CONTACT US/FEEDBACK":
    st.write("FOR ANY FURTHER QUERIES OR COMPLAINTS PLEASE ENTER THE INFORMATION ON THE FORM BELOW:")
     
    def is_valid_email(email):
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_pattern, email) is not None

    with st.form("contact_form"):
        name = st.text_input("First Name")
        email = st.text_input("Email Address")
        message = st.text_area("Your Message")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if not WEBHOOK_URL:
            st.error("Email service is not set up. Please try again later.", icon="📧")
            st.stop()

        if not name:
            st.error("Please provide your name.", icon="🧑")
            st.stop()

        if not email:
            st.error("Please provide your email address.", icon="📨")
            st.stop()

        if not is_valid_email(email):
            st.error("Please provide a valid email address.", icon="📧")
            st.stop()

        if not message:
            st.error("Please provide a message.", icon="💬")
            st.stop()

        
        data = {"email": email, "name": name, "message": message}
        response = requests.post(WEBHOOK_URL, json=data)

        if response.status_code == 200:
            st.success("Your message has been sent successfully! 🎉", icon="🚀")
        else:
            st.error("There was an error sending your message.", icon="😨")
    st.divider()
    st.write("PLEASE ENTER YOUR FEEDBACK BELOW")
    rating = st.slider("Rate our service:", min_value=1, max_value=5, step=1)
    
    if rating:
        st.markdown(f"You rated our service {rating} star(s).")
    
    st.write("THANK YOU FOR YOUR FEEDBACK")
    st.divider()
