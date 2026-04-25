import ollama
import json

def analyze_resume_llm(resume, jobs):
    try:
        resume_text = resume[:800]
        jobs_text = str(jobs[:2])

        prompt = f"""
Return ONLY JSON:

{{
  "score": number,
  "missing_skills": ["skill1", "skill2"],
  "suggestions": ["suggestion1", "suggestion2"]
}}

Resume:
{resume_text}

Jobs:
{jobs_text}
"""

        response = ollama.chat(
            model='phi3',
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2, "num_ctx": 1024},
            keep_alive=0
        )

        content = response['message']['content'].strip()

        try:
            return json.loads(content)
        except:
            start = content.find("{")
            end = content.rfind("}") + 1
            return json.loads(content[start:end])

    except Exception as e:
        return {
            "score": 0,
            "missing_skills": [],
            "suggestions": [f"Error: {str(e)}"]
        }


def improve_resume(resume):
    try:
        prompt = f"""
Improve this resume:

- Make ATS optimized
- Improve bullet points
- Add strong action verbs

Resume:
{resume[:800]}
"""

        response = ollama.chat(
            model='phi3',
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.3},
            keep_alive=0
        )

        return response['message']['content']

    except Exception as e:
        return f"Error: {str(e)}"