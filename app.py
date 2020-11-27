import matplotlib.pyplot    as plt
import numpy                as np
import pandas               as pd
import plotly.express       as px
import plotly.graph_objects as go
import streamlit            as st

def main():

    from datetime import time
    from PIL      import Image  as img

    def time_diff_(str1, str2):
        t_m1 = int(str1[:2])*60 + int(str1[-2:])
        t_m2 = int(str2[:2])*60 + int(str2[-2:])

        if(t_m1 > t_m2):
            td_m = t_m1-t_m2
            h = td_m // 60
            m = td_m - (h*60)
            if(m>9):
                return ("0"+str(h)+"h "+str(m)+ "min")
            else:
                return ("0"+str(h)+"h "+"0"+str(m) + "min")
        else:
            td_m = t_m2-t_m1
            h = td_m // 60
            m = td_m - h*60
            if(m>9):
                return ("0"+str(h)+"h "+str(m) + "min")
            else:
                return ("0"+str(h)+"h "+"0"+str(m)+ "min")

    def time_diff_nr_(str1, str2):
        t_m1 = int(str1[:2])*60 + int(str1[-2:])
        t_m2 = int(str2[:2])*60 + int(str2[-2:])

        return t_m1 - t_m2

    def time_sum_(str1, e):
        t_m1 = int(str1[:2])*60 + int(str1[-2:])
        t_m1 = t_m1+e

        h = t_m1 // 60
        m = t_m1 - (h*60)
        if(m>9):
            return (str(h)+":"+str(m))
        else:
            return (str(h)+":"+"0"+str(m))


    st.title("Toqua Smart Shipping")
    st.header("Use case - two barges passing Sluis Wijnegem")
    st.markdown("""Let us look at the use case where two barges depart from the docs of Antwerp.
    They both leave around 8:30, but each has a different destination:
    - barge A goes to Hasselt
    - barge B goes to Lommel

    These are the routes and tota travel times for both barges.
    """
    )

    route1 = img.open("route1.png")
    route2 = img.open("route3.png")

    col1, col2 = st.beta_columns(2)
    with col1:
        st.image(route1, use_column_width=True, caption="Route 1")
    with col2:
        st.image(route2, use_column_width=True, caption="Route 2")

    col3, col4 = st.beta_columns(2)
    with col3:
        st.markdown("Total travel time = 7u 22min")
    with col4:
        st.markdown("Total travel time = 9u 3min")

    st.markdown("(*info obtained from:* https://www.visuris.be/reisplanner)")

    st.markdown("""Today, both barges would arrive in about 1 hour at the Sluis Wijnegem,
    without knowing anything about each other's agenda.
    They would both navigate to Sluis Wijnegem as fast as they can, thereby wasting fuel,
    because they'll have to wait anyway.
    """)

    st.markdown("""Now imagine that instead of choosing when to leave, where to go and at what speed,
    the barges listen to a central platform for this information. They would have to tell
    at what time they have to arrive at their destinations (which will be checked with the
    terminals, to avoid fraud).
    Depending on who's most in a hurry, the order in which they pass will differ.
    The barges with no hurry will be told to navigate more slowly, thereby saving fuel and
    arriving just in time at Sluis Wijnegem to be served.
    """)

    st.markdown("""*Change the arrival time goals and see who is in a hurry or has time to spare.*
    """)

    arr_times = ["14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00"]
    etaA = "15:52"
    etaB = "17:33"

    col5, col6 = st.beta_columns(2)
    with col5:
        agA = st.select_slider(label="Barge A arrival time goal", options=arr_times, value="16:00")
        st.markdown("ETA = 15:52   |   arrival time goal = " + agA)
        if(agA > etaA):
            st.markdown(f'**Barge A has {time_diff_(etaA, agA)} to spare**')
        else:
            st.markdown(f'**Barge A has {time_diff_(etaA, agA)} to make up**')

    with col6:
        agB = st.select_slider(label="Barge B arrival time goal", options=arr_times, value="17:30")
        st.markdown("ETA = 17:33   |   arrival time goal = " + agB)
        if(agB > etaB):
            st.markdown(f'**Barge B has {time_diff_(etaB, agB)} to spare**')
        else:
            st.markdown(f'**Barge B has {time_diff_(etaB, agB)} to make up**')

        
    if (time_diff_nr_(agA, etaA) > time_diff_nr_(agB, etaB)):
        st.markdown('### Barge A is in less of a hurry, barge B can cross first.')
        sb = "A"
    else:
        st.markdown('### Barge B is in less of a hurry, barge A can cross first.')
        sb = "B"

    st.markdown("""Let's say that normally the barges navigate at 10km/h (the route from Antwerp to Sluis Wijnegem is 10km).
    We now want to slow down the barge that is to cross secondly, in order to make it save fuel and arrive just in time.
    We will tell it to slow down, depending on the time it takes for the first barge to cross the Sluis.
    """)

    st.markdown("""*Change the time it takes to cross Sluis Wijnegem and see what speed the second barge should use.*
    """)
    swt = st.radio("Time to cross Sluis Wijnegem", ("15min", "20min", "30min"))

    if (swt=="15min"):
        sp = "8km/h"
        e=15
        f="20%"
    elif (swt=="20min"):
        sp = "7,5km/h"
        e=20
        f="25%"
    elif (swt=="30min"):
        sp = "6,6km/h"
        e=30
        f="34%"

    new_etaA = time_sum_(etaA, e)
    new_etaB = time_sum_(etaB, e)

    st.markdown(f"### Barge {sb} should navigate at {sp}.")    
    st.markdown(f"### This leads to {f} more fuel efficiency.")
    if (sb == "A"):
        st.markdown(f"At this speed, barge {sb} will arive just in time at Sluis Wijnegem to cross. It's new ETA is {new_etaA}.")
        if (time_diff_nr_(agA, new_etaA) > 0):
            ac = "spare"
        else:
            ac = "make up"
        st.markdown(f"**Barge {sb} now has {time_diff_(agA, new_etaA)} to {ac}.**")
    else:
        st.markdown(f"At this speed, the barge {sb} will arive just in time at Sluis Wijnegem to cross. It's new ETA is {new_etaB}.")
        if (time_diff_nr_(agB, new_etaB) > 0):
            ac = "spare"
        else:
            ac = "make up"
        st.markdown(f"**Barge {sb} now has {time_diff_(agB, new_etaB)} to {ac}.**")

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

    if (e==15):
        fig = go.Figure(data=go.Scatter(x=x, y=y), layout=go.Layout(title=go.layout.Title(text="Speed fuel curve")))
        fig = fig.update_layout(shapes=[
            dict(
            type= 'line',
            yref= 'paper', y0= 0, y1= 1,
            xref= 'x', x0= 10, x1= 10,
            line=dict(
                            color="black",
                            width=4,
                            dash="dash",
                        )
            ),
            dict(
            type= 'line',
            yref= 'paper', y0= 0, y1= 1,
            xref= 'x', x0= 8, x1= 8,
            line=dict(
                            color="green",
                            width=4,
                            dash="dash",
                        )
            )
        ])
        fig = fig.update_layout(xaxis_title="speed", yaxis_title="fuel")
        st.plotly_chart(fig)
    elif (e==20):
        fig = go.Figure(data=go.Scatter(x=x, y=y), layout=go.Layout(title=go.layout.Title(text="Speed fuel curve")))
        fig = fig.update_layout(shapes=[
            dict(
            type= 'line',
            yref= 'paper', y0= 0, y1= 1,
            xref= 'x', x0= 10, x1= 10,
            line=dict(
                            color="black",
                            width=4,
                            dash="dash",
                        )
            ),
            dict(
            type= 'line',
            yref= 'paper', y0= 0, y1= 1,
            xref= 'x', x0= 7.5, x1= 7.5,
            line=dict(
                            color="green",
                            width=4,
                            dash="dash",
                        )
            )
        ])
        fig = fig.update_layout(xaxis_title="speed", yaxis_title="fuel")
        st.plotly_chart(fig)
    elif (e==30):
        fig = go.Figure(data=go.Scatter(x=x, y=y), layout=go.Layout(title=go.layout.Title(text="Speed fuel curve")))
        fig = fig.update_layout(shapes=[
            dict(
            type= 'line',
            yref= 'paper', y0= 0, y1= 1,
            xref= 'x', x0= 10, x1= 10,
            line=dict(
                            color="black",
                            width=4,
                            dash="dash",
                        )
            ),
            dict(
            type= 'line',
            yref= 'paper', y0= 0, y1= 1,
            xref= 'x', x0= 6.6, x1= 6.6,
            line=dict(
                            color="green",
                            width=4,
                            dash="dash",
                        )
            )
        ])
        fig = fig.update_layout(xaxis_title="speed", yaxis_title="fuel")
        st.plotly_chart(fig)



    st.markdown("## Conclusion")
    st.markdown("""What this interactive toy example means to show is that having a centralized platform, that
    has data about all ships, terminals and objects in the network, can optimize corridor management globally.
    Individuals can benefit from this global optimum, and at least they will not have drawbacks of it.
    In our example we saw that barges in a hurry will make up for lost time more easily, while others that now have
    to wait, do not loose more time than without the knowledge, but they do save fuel, and arrive just in time.
    """)

if __name__ == '__main__':
    main()