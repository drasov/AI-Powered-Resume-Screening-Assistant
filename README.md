1.0 Problem Statement: The Resumé Screening Bottleneck
Most companies have tons of applications for each and every job opening. The old ways of having someone skim over each applicant are now seen as highly inefficient and outdated. Since most recruiters have begun to implement AI in some way or another, the process has begun to see leaps in efficiency and time saved. A recruiter used to have spent an average of 23 seconds per resumé[1], yet, also have been prone to human bias and error. Since manual screening creates large bottlenecks, 73% of recruiters stating it as their biggest loss in time which caused them to delay on hires and potentially losing their top talent to the competition[2]. 

2.0 The AI Imperative: Why Now?
The shift of AI driven screening is not a far cry anymore, by the end of 2025, 83% of companies are projected to have implemented AI to screen their resumés, which is a massive increase from a mere 48% in 2024[3]. The change has been caused by a desire for efficiency and the rapid improvement of AI. Considering AI can reduce the time to screen a resumé by up to 75% and see improvements from roughly 70-90% compared to those screened by a human[4]. Additionally, 67% of companies admit to having AI bias in their screening yet continue to use their methods due to the increasingly positive returns from the efficiency gained[5]. This paradoxical situation provides a crucial gap in the market for a solution that is both ethical and efficient while most importantly, being built from the ground up.

3.0 Our Solution: An Intelligent and Context-Aware AI Assistant
Our group is developing an AI powered resumé screening assistant that applies NLP (Natural Language Processing) and ML (Machine Learning) to push past the rigid, keyword based filters[6] seen in current screening processes. Our system is designed to not only comprehend the context of the user's experience, but also infer their proficiency. For example, a sentence read as “Created & deployed a single-page application using React,” will have the assistant understand that  the user knows React, JS, and CSS; knows how CI/CD works and knows how to deploy a project. This will allow for identifying transferable skills and creating a more accurate assessment of each applicant[7]. The core to our solution lies in the ability to extract key details and parse through important information such as skills and experience, while also ranking candidates based on a series of conditions to best find a true match for the job’s requirements[8].
4.0 Technology Stack: Built on a Modern, Robust Foundation
We will build this solution using a proven, professional technology stack:

Core AI & NLP: We will utilize spaCy for efficient Named Entity Recognition (NER) to extract skills, qualifications, and experience. We will also explore fine tuning a BERT-class model for superior semantic understanding, moving beyond simple keyword matching[9].
Frameworks & Development: Python will serve as the core language, with Flask or FastAPI for the backend API and React for an intuitive frontend user interface.
Data & Storage: Pandas will be used for data manipulation and MongoDB or PostgreSQL for secure data storage.
5.0 System Architecture: A Cohesive and Scalable Workflow
The system is designed with a clear, modular architecture for reliability and scalability:

Frontend (React Web Application): A clean, intuitive dashboard for recruiters to upload job descriptions and resumés.
Backend (Flask/FastAPI Server): The engine that handles requests, processes files, and manages communication between the frontend and the AI model.
AI Model (NLP Engine): The core intelligence that analyzes text, extracts skills, and calculates match scores using machine learning algorithms[10].
Database (MongoDB/PostgreSQL): Securely stores anonymized applicant data and matching results.

Data Flow: Recruiter Uploads Data -> Backend Preprocesses Text -> AI Model Analyzes & Compares -> Backend Ranks Candidates -> Results Displayed on Dashboard
6.0 Data and Ethical Considerations: Building a Responsible Tool
We are committed to developing this technology with a focus on fairness and privacy.

Mitigating Bias: We will  proactively address the well-documented risk of AI bias, where studies show tools can favor white associated names 85% of the time and male-associated names 52% of the time[11]. Our approach includes regular algorithm audits, the use of diverse datasets, and features to anonymize candidate data, helping to focus evaluation on qualifications[12].
Privacy & Security: Candidate privacy is paramount. We will implement a strict data retention policy, ensuring that original resumé files are securely deleted after processing. All data will be encrypted in transit and at rest.
Human-in-the-Loop: Recognizing that AI cannot assess soft skills or cultural fit, our solution is designed to augment—not replace—recruiters. It provides a ranked shortlist, leaving the final selection to human judgement[13].

7.0 Conclusion: Our AI powered resumé Screening Assistant displays an impactful and practical application of AI to a unique, modern day business challenge. By taking advantage of the demonstrated efficiency gains seen by implementing AI, which can save up to 10 hours per 100 resumés reviewed[14]. We can help organizations find smarter talent quicker. While, more importantly, having a mitigated bias built into the core of our system, we offer a path to a more fair and consistent screening process, giving each and every candidate a more equal fighting chance while allowing the human experts to focus on the more interpersonal aspects of recruiting.

References
[1] LinkedIn Talent Solutions. (2023). 2023 Global Talent Trends Report.

[2] SHRM. (2024). The Cost of a Bad Hire. Society for Human Resource Management.

[3] Gartner. (2024). Predicts 2025: AI and the Future of Work.

[4] Deloitte Insights. (2024). AI in Hiring: From Hype to Reality.

[5] Harvard Business Review Analytic Services. (2024). The State of AI in Talent Acquisition.

[6] Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. Proceedings of NAACL-HLT.

[7] Honnibal, M., & Montani, I. (2017). spaCy: Industrial-Strength Natural Language Processing in Python. Explosion AI.

[8] Lample, G., Ballesteros, M., Subramanian, S., Kawakami, E., & Dyer, C. (2016). Neural Architectures for Named Entity Recognition. Proceedings of NAACL-HLT.

[9] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention Is All You Need. Advances in Neural Information Processing Systems.

[10] Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining.

[11] Raghavan, M., Barocas, S., Kleinberg, J., & Levy, K. (2020). Mitigating Bias in Algorithmic Hiring: Evaluating Claims and Practices. Proceedings of the FAT* Conference.

[12] Bogen, M., & Rieke, A. (2018). Help Wanted: An Examination of Hiring Algorithms, Equity, and Bias. Upturn.

[13] Wilson, H. J., & Daugherty, P. R. (2018). Collaborative Intelligence: Humans and AI Are Joining Forces. Harvard Business Review.

[14] Ideal. (2023). The Impact of AI on Recruitment Efficiency. Ideal White Paper.


