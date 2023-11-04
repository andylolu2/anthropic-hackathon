MAIN_PROMPT = """
Hi Claude, I am a medical expert analysing the quality of history taken by doctors. As part of the simulation, you will be asked to provide your thoughts to compare to mine.

Background:
You will read a consultation between a GP and a patient that has already happened. The patient starts by saying their initial story and what they would like help with. This is never enough to get to a full diagnosis. In fact the role of an excellent GP is to ask a series of very well phrased questions that most effectively and intelligently dissect the diagnostic search space to reach a set of most probable differential diagnoses, and most importantly to rule out differential diagnoses that are potentially life threatening to the patient, even if they are not the most likely. The conversation takes the form of a series of questions (asked by the doctor) and answers (from the patient).

Tasks:

Auxiliary task

As you read through the conversation, pause and think after each response from the patient. I want you to think of three things given the information you have at each point.
1. The top differential diagnoses that explain the symptoms the patient is describing.
2. The most dangerous diagnoses that even if unlikely could potentially fit the cluster of symptoms from the patient and that therefore you need to rule out
3. And most importantly, given these two differentials, what is the most informative next question/set of questions that will allow you to efficiently dissect the diagnostic search space, taking into account the dual task of
    1) find the most likely diagnosis, and
    2) rule out the most dangerous likely diagnoses. 

At each point, you will internally compare your next best question/set of questions with the clinician's actual question/set of questions.  

Main task

As the interaction continues and comes to an end, I want you to work out:
1. What are the most likely/dangerous diagnostic spaces/differential diagnoses that the doctor HAS or HAS NOT appropriately enquired about and ruled in or out. (For appropriately I mean that the patient's answer does not leave scope for misunderstanding, and if it does that it should be clarified.)
2. At the end of the consultation, the doctor will give their impression of what is going on, and the next steps they believe should be taken to further clarify what the underlying pathology or pathologies are. At this point, the doctor will ask you “Claude, do you have any further questions or thoughts?” 
3. At this point you will state the following: 
    1) The differential diagnoses
    2) 


Think of your own suggestion of what the next best question (or set of questions) that you believe the doctor should ask would narrow the diagnosis space given the conversation up to that point. At the end of the conversation, the GP will present their differential diagnoses as well as their plan for next best steps to narrow these down. Then, you will be prompted to give your input. Your input consists of suggesting questions and investigations or differential diagnoses that differ from that of the GP. Your input consists of a series of questions that you believe most effectively rule in or out important or dangerous differential diagnoses that the doctor has not explicitly ruled out.
""".strip()

CLEAN_HTML_PROMPT = """
Below is the HTML for a webpage on medical guidelines. Identify the main content of the page. Ignore all headings, footers, navigation blocks, and unimportant information. Try not to re-word the guidelines. Respond with a single whitespace if you don't think there is meaningful content (e.g. a 404 error / the HTML is not rendered properly).

<html>
{html}
</html>
""".strip()
