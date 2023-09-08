# EdControl

Automated analytics service that tracks students' emotional responses during online classes.

## Problem

Today, there are a large number of platforms for online learning. There are both large online schools and smaller ones in terms of the number of students. And because of the large flow of clients, it is necessary to recruit teachers to conduct classes. And managers can not always understand how much the teacher is competent in the field of soft skills when submitting material. Therefore, it is necessary to identify aggressive and unable to control their emotions teachers in time to preserve the reputation of the company.

## Solving the problem

Our product offers a solution to this problem of education assessment, helping online platforms save managers' time when manually viewing teachers' video lessons and improve the company's business metrics by identifying non-competent teachers at an early stage. The problem is solved by recognizing the client's negative emotions during an online lesson with a teacher. You upload a video lesson recording to our service and get a dashboard with information and analytics throughout the lesson. Also on this dashboard, when identifying any negative situations, you can see the specific timestamp when the emotion was noticed and how big it is.

## Implementation

Currently implemented:
- Emotional assessment of a person's condition
- Data analytics and visualization for convenient video lesson analysis
- Recommendations to the teacher for subsequent lessons, if any problems are found

The CV model determines the emotion that a person is experiencing at a given time and displays the depth of emotion on a scale from 0 to 100:

girl.png
boy.png



## The appearance of the service

The appearance of the service is intuitive for users and its main page looks like this:
3.png

After successfully processing the uploaded video, you can get analytics and recommendations:
1.png

## Road Map

At the moment, the product is in working condition and ready for use. Our EdControl team sees prospects and the further path of product development, the addition of new features and the expansion of the target audience.

- Cutting out a window with students
- Adding speech recognition (text) and intonation (audio) to improve the accuracy of determining the emotional state
- Adding recognition of ban words and gestures
- Adding face identification function
- Adding the ability to recognize the emotional state in group calls and conferences
- Integration into LMS systems of various platforms