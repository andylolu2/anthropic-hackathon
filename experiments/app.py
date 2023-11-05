from llm_diag import DiagnosisLLM

if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=5000)
    transcript = """

Exploration:



Doctor  00:11
Hi, my name is Dr. Conci. I'm one of the medical registrars here on the medical take.
What's your name again? 

Patient 00:16
My name is Ricardo.
I've come because I haven't been feeling so well lately.
Basically, some there are moments where I get these really weird feelings on my chest like it feels like my heart is pounding.
And sometimes I get quite dizzy with it.
And I don't Yeah, I've sort of not thought about it much. But then the other day I was I felt really lightheaded really dizzy, and I and the heart was going and I sort of thought, okay, maybe this is something I should come and check out.

Doctor  01:01
Okay, okay. Thank you for coming to see ys today. I think it's really important that we get it checked out. Can you tell me a little bit more about how it started and when it started.

Patient  01:12
So happened so about, like two, three months ago, I had COVID and it was fairly mild.
I just yeah, had Covid and then I recovered quite well. And then I think it was after you know, after that that thing started to get a bit worse. When I first noticed it, it was quite mild, and it sort of went away for after a few seconds to maybe a minute.
And then it sort of nothing happened for maybe a week. Or two. And then I think maybe I was doing some exercise. I was like running out running and then again I felt it and then I sort of stopped and and I felt I was feeling a little bit lightheaded at that point, which is why I sort of stopped but I don't know because I feel like there's been a lot going on as well. Recently, I had my big exams, which I'm sort of still quite stressed about because I still got more going on.
So I haven't been sort of living the most healthy of lives as it were. Lots of Red Bull and coffee.
I know that's not great. But yeah, so I don't know. That's sort of that.

Doctor  02:30
okay, so thank you. Thank you for sharing your thoughts as well. Is there anything in particular you concerned this might be?

Patient   02:38
Well, I don't know. I mean, I know that my someone from like my family-  my uncle from my dad's side and and some of my cousins and I'm not sure about my dad, but I feel like they've they've had some heart issues before.
I don't remember exactly what but obviously when knowing that that's been the case, and that I had something that maybe feels like it's my heart. It made me quite worried about it. So I don't know what but I think that that concerned me.

Doctor  03:12
Okay. So thank you for sharing that. Do you mind if I ask you a few more questions about the heart racing in particular and then I can ask you a few more questions about your lifestyle in general and your personal history. Would that be okay?

Patient  03:30
Okay.

Doctor  03:32
And just checking, It's only heart racing and feeling a little dizzy that you've experienced? There is no other symptoms that you're worried about that you'd like to mention?

Patient  03:41
No, no, I mean, sometimes I'm like, I feel quite short of breath with this heart racing thing.
But But um, no, otherwise if I've been okay, I think Yeah.

Doctor  03:55
So if we start with the heart racing. So you mentioned that you think it started when you had COVID? Correct? 

Patient 
Yeah, or just I think just after COVID. 

Doctor 
Just after COVID. And you mentioned that you've thought the duration of your episodes were about seconds to minutes long. 

Patient
Yeah, yeah. Yeah. So yeah, seconds, two minutes. I did say probably about a minute each time. You know, I I tried to clock it once, but I think it was around a minute or two.

Doctor  04:23
Okay. Has that changed at all? With time?

Patient  04:28
Ah, I don't think so? No.

Doctor  04:37
And the frequency in which you were having these episodes initially, you said it was quite sporadic.
Is that still the case? Or have you managed to, you know, undercover a pattern?

Patient  04:49
Yeah, it's that's a good question.
I feel like it tends to happen when I'm maybe more stressed, or maybe when I'm doing some exercise.
It has sort of been happening a little bit more frequently recently. Which is also why I really wanted to come in.

Doctor  05:10
So in a day, how often might it happen?

Patient  05:15
Initially, it was happening once every 2,3,4 days.
Now it's it's more like once a day, sometimes more, maybe multiple times a day.

Doctor  05:30
Is there anything that you think might trigger it in particular in activity or could be also when you're just lying in bed resting?

Patient  05:40
Yeah, I think it has happened. I you know, I don't know. I don't know. Actually, I feel like it has happened once they've been resting, but it tends to be more when I'm doing something.

Doctor  05:52
Okay, no problem.
And when it happens, can you tap out how it feels like in your chest?

Patient  06:02
It's it feels a little bit heavy on my chest, and it feels quite like it like the heart is beating really hard. And it feels a little bit and faster than normal. 

Doctor
Are you skipping beats? Do you feel like your heart is beating irregularly?

Patient  06:29
I I haven't paid attention to that. I don't know.

Doctor  06:36
And did you think you might be able to tap on your chest how it feels like how fast that can go? 

Patient 
Yeah. Something like pat pat pat pat pat... that sort of thing.

Doctor  06:51
Okay. Okay.
Okay. And when you heard these episodes, you mentioned that sometimes you also feel dizzy with do you mean lightheaded? Like you might be passing out or potentially could pass out if it was continuing your longer? 

Patient
Yes, that's that's exactly what I meant. 

Doctor
Yeah. Okay. And have you ever passed out?

Patient
Yeah I did, I I was next to my bed. So I think I must have sort of got to the bed, hit the bed, and then just sort of recovered quite quickly.
I didn't think I was out for very long

Doctor  07:44
do you feel like you might have lost consciousness at all in that period of time?

Patient  07:49
Maybe for a few seconds. Yeah.

Doctor  07:53
And what were you doing at that particular moment? Just before this happened?

Patient  08:01
I think I was I was running back to my flat.
And I was quite stressed because I was rushing for something. And I would just run up the stairs and I got to my bedroom and then and that's sort of when it happened and that's when I fell on the bed.

Doctor  08:22
Okay.
Thank you for thank you for sharing. Do you have any chest pain at all normally, when you have these episodes? 

Patient
Yeah, I don't know if it's pain but it feels a little bit tight around. It feels like I'm sort of constricted breathing

Doctor  08:43
do you ever feel yourself wheezing or having shortness of breath?

Doctor  08:50
Yeah, so no wheeze, I did used to have asthma as a kid but but no wheeze; and shortness of breath, I mean, I guess a little bit more since I've been having this. 
And obviously when I get the palpitations and I do feel quite short of breath. Yeah.

Doctor  09:10
But you're not actively wheezing at the moment?

Patient
exactly I'm not actively wheezing. No.

Doctor  09:17
Okay, good. A few more questions if that's okay.
So, do you eat and drink normally?
Normal weight? I'm assuming you have a normal BMI?

Patient
Yeah, I'm I trying to keep myself fit. I don't do a huge amount of exercise. I have to say I haven't been eating super well and sleeping super well recently because of these exams.
I'm also trying to quit smoking, which I know is not good, but you know, yeah. It's been quite difficult recently.

Doctor  09:58
In terms of your lifestyle, how many cigarettes do you smoke in a day?

Patient  10:03
I try to keep it under maybe five to 10 but on bad days it goes up to maybe 20.

Doctor  10:15
And in terms of caffeine intake how much might it be in a day?

Patient  10:21
Yeah, recently quite a lot. To be honest. I'm I'm really trying to work a lot, do quite a lots of hours.
During the day much, I'll have maybe three to like maybe two or three coffees in the day. I think so one in the morning, one around mid like just before lunch and one in sort of early afternoon.

Doctor  10:44
Okay.
And any alcohol at all?

Patient
 No, actually, it's, ya know, not much other than the occasional party, but you know, 

Doctor
any recreational drugs?

Patient  11:01
I feel like that's, that will probably happen more after exams.
But by no not Not, not in the last two months.

Doctor  11:10
So not related to these symptoms.

Patient  11:14
Well, actually, now you mentioned it.. Okay, no, I I should have said, I did a sort of stimulant drug about three weeks ago, and that then that sort of brought it on as well.

Doctor  11:39
Was that something to help with performance in exams? 

Patient
Yeah, exactly. Yeah. Yeah.

Doctor  11:48
It might be wise to avoid caffeine and stimulants. It's a bit concerning that you've had an episode of passing out. 
But I'll ask you a few questions to rule out any big things. 
You haven't noticed any bleeding whatsoever from anywhere? So not coughing any blood and not peeing any blood and pooing any blood or black stools? 

Patient
No, no, no, 

Doctor
that's okay. You don't normally feel dizzy when you stand up from lying?

Patient  12:20
No, no.

Doctor  12:23
Okay, good. You haven't had any fevers?

Patient  12:26
No, I mean, I had COVID. But then after that, it's no no fevers. 

Doctor
Okay, and you're not finding yourself unintentionally loosing weight? Your eyes bulging out more than normal? Your appearance changing? Hands being sweaty? 

Patient
Oh, gosh.
No, I don't think so. Yeah, sounds like a big change.

Doctor  12:50
Ok. I'm going to keep ruling out a few more things in the meantime. So you haven't had any episodes of you know, coughing up blood or anything like that.

Patient
No

Doctor  13:00
And in terms of your past medical history, you mentioned you have a asthma.
Do you have any other diagnoses? any previous surgeries? Any recent long haul flights?

Patient  13:17
Oh, good question. So,I have had some surgery, When I was much younger. I broke my wrist.

But then in terms of... Actually just around COVID as well I was coming back from a long haul flight. I think that's where I got the COVID from actually.
So yeah.

Doctor  13:50
But okay. Do you mind me asking how long was that flight?

Patient  13:54
It was it was quite long as maybe eight hours or so.

Doctor  13:59
Yeah, how many? Eight hours? 

Patient
Eight hours.

Doctor  14:05
And you haven't noticed any cough swelling or tenderness at that time when he first started?

Patient  14:14
No, no, I don't think so.

Doctor  14:17
No, ok brilliant.
Great. So thank you for answering all those questions that I can appreciate that amongst be quite concerning to have these palpitations. 
you mentioned you have a family history that you concerned about and they might have something to do with the heart. Do you have any more information about that?

Patient  14:38
I I'm not sure but I can ask I think yeah, I mean, my uncle had a heart attack when he was I think in his 40s and and I'm not really sure about my dad or my cousin, but I know they've had some issues.

Doctor  15:02
Okay, any diabetes or cancer in the family?

Patient  15:08
My mom has diabetes.
But no cancer. Luckily okay. 


Doctor
Any history of high blood pressure?

Patient  15:21
I think my mom is on blood pressure tablets as well. Yeah. And

Doctor
Any history of blood clots?

Patient  15:30
I don't know. I don't know. Sorry.

Doctor  15:33
No problem.
Great. And just to check, other than the stimulant you took a few weeks ago you aren't on any regular medications? 

Patient
No, I mean, yeah, sometimes some paracetamol to help my headaches, but no I haven't tried anything.

Doctor  16:03
So fantastic, so now I think would be a good time for me to examine you if that's ok. 
We'll take some blood tests, do an ECG and I would also be quite interested in doing an echocardiogram, a jelly scan of your heart, to make sure there isn't anything that can be causing you feeling palpitations on exercise. 

It may be the case that we'll call you back to do some exercise testing whilst you're being monitored, if that's ok. And sometimes what we can do is, in the meantime, we record your heart remotely. So we put you on what's called a Holter monitor, just to be able to pick up those episodes of palpitations because you mentioned it can happen sometimes a few times a day and maybe they can be captured, Especially when you are recording for three to seven days.

Yeah, I should probably mention in the blood test we will do some routine bloods to make sure that you're not bleeding, make sure you don't have any infection and to make sure that your hormone levels, especially your thyroid, are normal.

There is one thing I forgot to ask you about, that sometimes we check, especially with students who might be stressed; there is no chance that you might be inducing yourself to vomit? or anything like that? Sometimes that can cause people to feel quite weak and make their heart race as well. 

Patient
Yeah, that's a good question. No, I, I used to have an issue with that but not not anymore.

Doctor  17:36
If you did encounter that issue, again, during some periods, I can send you some leaflets that can be quite helpful. 
Claude, do you have any further questions or thoughts




Doctor  00:11
Hi, my name is Dr. Conci. I'm one of the medical registrars here on the medical take.
What's your name again? 

Patient 00:16
My name is Ricardo.
I've come because I haven't been feeling so well lately.
Basically, some there are moments where I get these really weird feelings on my chest like it feels like my heart is pounding.
And sometimes I get quite dizzy with it.
And I don't Yeah, I've sort of not thought about it much. But then the other day I was I felt really lightheaded really dizzy, and I and the heart was going and I sort of thought, okay, maybe this is something I should come and check out.

Doctor  01:01
Okay, okay. Thank you for coming to see ys today. I think it's really important that we get it checked out. Can you tell me a little bit more about how it started and when it started.

Patient  01:12
So happened so about, like two, three months ago, I had COVID and it was fairly mild.
I just yeah, had Covid and then I recovered quite well. And then I think it was after you know, after that that thing started to get a bit worse. When I first noticed it, it was quite mild, and it sort of went away for after a few seconds to maybe a minute.
And then it sort of nothing happened for maybe a week. Or two. And then I think maybe I was doing some exercise. I was like running out running and then again I felt it and then I sort of stopped and and I felt I was feeling a little bit lightheaded at that point, which is why I sort of stopped but I don't know because I feel like there's been a lot going on as well. Recently, I had my big exams, which I'm sort of still quite stressed about because I still got more going on.
So I haven't been sort of living the most healthy of lives as it were. Lots of Red Bull and coffee.
I know that's not great. But yeah, so I don't know. That's sort of that.

Doctor  02:30
okay, so thank you. Thank you for sharing your thoughts as well. Is there anything in particular you concerned this might be?

Patient   02:38
Well, I don't know. I mean, I know that my someone from like my family-  my uncle from my dad's side and and some of my cousins and I'm not sure about my dad, but I feel like they've they've had some heart issues before.
I don't remember exactly what but obviously when knowing that that's been the case, and that I had something that maybe feels like it's my heart. It made me quite worried about it. So I don't know what but I think that that concerned me.

Doctor  03:12
Okay. So thank you for sharing that. Do you mind if I ask you a few more questions about the heart racing in particular and then I can ask you a few more questions about your lifestyle in general and your personal history. Would that be okay?

Patient  03:30
Okay.

Doctor  03:32
And just checking, It's only heart racing and feeling a little dizzy that you've experienced? There is no other symptoms that you're worried about that you'd like to mention?

Patient  03:41
No, no, I mean, sometimes I'm like, I feel quite short of breath with this heart racing thing.
But But um, no, otherwise if I've been okay, I think Yeah.

Doctor  03:55
So if we start with the heart racing. So you mentioned that you think it started when you had COVID? Correct? 

Patient 
Yeah, or just I think just after COVID. 

Doctor 
Just after COVID. And you mentioned that you've thought the duration of your episodes were about seconds to minutes long. 

Patient
Yeah, yeah. Yeah. So yeah, seconds, two minutes. I did say probably about a minute each time. You know, I I tried to clock it once, but I think it was around a minute or two.

Doctor  04:23
Okay. Has that changed at all? With time?

Patient  04:28
Ah, I don't think so? No.

Doctor  04:37
And the frequency in which you were having these episodes initially, you said it was quite sporadic.
Is that still the case? Or have you managed to, you know, undercover a pattern?

Patient  04:49
Yeah, it's that's a good question.
I feel like it tends to happen when I'm maybe more stressed, or maybe when I'm doing some exercise.
It has sort of been happening a little bit more frequently recently. Which is also why I really wanted to come in.

Doctor  05:10
So in a day, how often might it happen?

Patient  05:15
Initially, it was happening once every 2,3,4 days.
Now it's it's more like once a day, sometimes more, maybe multiple times a day.

Doctor  05:30
Is there anything that you think might trigger it in particular in activity or could be also when you're just lying in bed resting?

Patient  05:40
Yeah, I think it has happened. I you know, I don't know. I don't know. Actually, I feel like it has happened once they've been resting, but it tends to be more when I'm doing something.

Doctor  05:52
Okay, no problem.
And when it happens, can you tap out how it feels like in your chest?

Patient  06:02
It's it feels a little bit heavy on my chest, and it feels quite like it like the heart is beating really hard. And it feels a little bit and faster than normal. 

Doctor
Are you skipping beats? Do you feel like your heart is beating irregularly?

Patient  06:29
I I haven't paid attention to that. I don't know.

Doctor  06:36
And did you think you might be able to tap on your chest how it feels like how fast that can go? 

Patient 
Yeah. Something like pat pat pat pat pat... that sort of thing.

Doctor  06:51
Okay. Okay.
Okay. And when you heard these episodes, you mentioned that sometimes you also feel dizzy with do you mean lightheaded? Like you might be passing out or potentially could pass out if it was continuing your longer? 

Patient
Yes, that's that's exactly what I meant. 

Doctor
Yeah. Okay. And have you ever passed out?

Patient
Yeah I did, I I was next to my bed. So I think I must have sort of got to the bed, hit the bed, and then just sort of recovered quite quickly.
I didn't think I was out for very long

Doctor  07:44
do you feel like you might have lost consciousness at all in that period of time?

Patient  07:49
Maybe for a few seconds. Yeah.

Doctor  07:53
And what were you doing at that particular moment? Just before this happened?

Patient  08:01
I think I was I was running back to my flat.
And I was quite stressed because I was rushing for something. And I would just run up the stairs and I got to my bedroom and then and that's sort of when it happened and that's when I fell on the bed.

Doctor  08:22
Okay.
Thank you for thank you for sharing. Do you have any chest pain at all normally, when you have these episodes? 

Patient
Yeah, I don't know if it's pain but it feels a little bit tight around. It feels like I'm sort of constricted breathing

Doctor  08:43
do you ever feel yourself wheezing or having shortness of breath?

Doctor  08:50
Yeah, so no wheeze, I did used to have asthma as a kid but but no wheeze; and shortness of breath, I mean, I guess a little bit more since I've been having this. 
And obviously when I get the palpitations and I do feel quite short of breath. Yeah.

Doctor  09:10
But you're not actively wheezing at the moment?

Patient
exactly I'm not actively wheezing. No.

Doctor  09:17
Okay, good. A few more questions if that's okay.
So, do you eat and drink normally?
Normal weight? I'm assuming you have a normal BMI?

Patient
Yeah, I'm I trying to keep myself fit. I don't do a huge amount of exercise. I have to say I haven't been eating super well and sleeping super well recently because of these exams.
I'm also trying to quit smoking, which I know is not good, but you know, yeah. It's been quite difficult recently.

Doctor  09:58
In terms of your lifestyle, how many cigarettes do you smoke in a day?

Patient  10:03
I try to keep it under maybe five to 10 but on bad days it goes up to maybe 20.

Doctor  10:15
And in terms of caffeine intake how much might it be in a day?

Patient  10:21
Yeah, recently quite a lot. To be honest. I'm I'm really trying to work a lot, do quite a lots of hours.
During the day much, I'll have maybe three to like maybe two or three coffees in the day. I think so one in the morning, one around mid like just before lunch and one in sort of early afternoon.

Doctor  10:44
Okay.
And any alcohol at all?

Patient
 No, actually, it's, ya know, not much other than the occasional party, but you know, 

Doctor
any recreational drugs?

Patient  11:01
I feel like that's, that will probably happen more after exams.
But by no not Not, not in the last two months.

Doctor  11:10
So not related to these symptoms.

Patient  11:14
Well, actually, now you mentioned it.. Okay, no, I I should have said, I did a sort of stimulant drug about three weeks ago, and that then that sort of brought it on as well.

Doctor  11:39
Was that something to help with performance in exams? 

Patient
Yeah, exactly. Yeah. Yeah.

Doctor  11:48
It might be wise to avoid caffeine and stimulants. It's a bit concerning that you've had an episode of passing out. 
But I'll ask you a few questions to rule out any big things. 
You haven't noticed any bleeding whatsoever from anywhere? So not coughing any blood and not peeing any blood and pooing any blood or black stools? 

Patient
No, no, no, 

Doctor
that's okay. You don't normally feel dizzy when you stand up from lying?

Patient  12:20
No, no.

Doctor  12:23
Okay, good. You haven't had any fevers?

Patient  12:26
No, I mean, I had COVID. But then after that, it's no no fevers. 

Doctor
Okay, and you're not finding yourself unintentionally loosing weight? Your eyes bulging out more than normal? Your appearance changing? Hands being sweaty? 

Patient
Oh, gosh.
No, I don't think so. Yeah, sounds like a big change.

Doctor  12:50
Ok. I'm going to keep ruling out a few more things in the meantime. So you haven't had any episodes of you know, coughing up blood or anything like that.

Patient
No

Doctor  13:00
And in terms of your past medical history, you mentioned you have a asthma.
Do you have any other diagnoses? any previous surgeries? Any recent long haul flights?

Patient  13:17
Oh, good question. So,I have had some surgery, When I was much younger. I broke my wrist.

But then in terms of... Actually just around COVID as well I was coming back from a long haul flight. I think that's where I got the COVID from actually.
So yeah.

Doctor  13:50
But okay. Do you mind me asking how long was that flight?

Patient  13:54
It was it was quite long as maybe eight hours or so.

Doctor  13:59
Yeah, how many? Eight hours? 

Patient
Eight hours.

Doctor  14:05
And you haven't noticed any cough swelling or tenderness at that time when he first started?

Patient  14:14
No, no, I don't think so.

Doctor  14:17
No, ok brilliant.
Great. So thank you for answering all those questions that I can appreciate that amongst be quite concerning to have these palpitations. 
you mentioned you have a family history that you concerned about and they might have something to do with the heart. Do you have any more information about that?

Patient  14:38
I I'm not sure but I can ask I think yeah, I mean, my uncle had a heart attack when he was I think in his 40s and and I'm not really sure about my dad or my cousin, but I know they've had some issues.

Doctor  15:02
Okay, any diabetes or cancer in the family?

Patient  15:08
My mom has diabetes.
But no cancer. Luckily okay. 


Doctor
Any history of high blood pressure?

Patient  15:21
I think my mom is on blood pressure tablets as well. Yeah. And

Doctor
Any history of blood clots?

Patient  15:30
I don't know. I don't know. Sorry.

Doctor  15:33
No problem.
Great. And just to check, other than the stimulant you took a few weeks ago you aren't on any regular medications? 

Patient
No, I mean, yeah, sometimes some paracetamol to help my headaches, but no I haven't tried anything.

Doctor  16:03
So fantastic, so now I think would be a good time for me to examine you if that's ok. 
We'll take some blood tests, do an ECG and I would also be quite interested in doing an echocardiogram, a jelly scan of your heart, to make sure there isn't anything that can be causing you feeling palpitations on exercise. 

It may be the case that we'll call you back to do some exercise testing whilst you're being monitored, if that's ok. And sometimes what we can do is, in the meantime, we record your heart remotely. So we put you on what's called a Holter monitor, just to be able to pick up those episodes of palpitations because you mentioned it can happen sometimes a few times a day and maybe they can be captured, Especially when you are recording for three to seven days.

Yeah, I should probably mention in the blood test we will do some routine bloods to make sure that you're not bleeding, make sure you don't have any infection and to make sure that your hormone levels, especially your thyroid, are normal.

There is one thing I forgot to ask you about, that sometimes we check, especially with students who might be stressed; there is no chance that you might be inducing yourself to vomit? or anything like that? Sometimes that can cause people to feel quite weak and make their heart race as well. 

Patient
Yeah, that's a good question. No, I, I used to have an issue with that but not not anymore.

Doctor  17:36
If you did encounter that issue, again, during some periods, I can send you some leaflets that can be quite helpful. 

Patient  17:47
That's fine. Thank you.

Doctor  17:50
Okay, well, thank you. It's lovely to meet you.

Patient
Thank you!

    """
    LLM = DiagnosisLLM()
    LLM.init_extraction_chains()
    LLM.extract_from_transcript(transcript)
    LLM.init_conv_chain()
    out = LLM.answer_doctor_query("investigate")
    print(out)
