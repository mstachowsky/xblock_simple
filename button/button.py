"""TO-DO: Write a description of what this XBlock is."""

from importlib.resources import files
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
from xblock.runtime import Runtime

import os
import requests
import json
import traceback

class ButtonXBlock(XBlock):
    """
    XBlock for writing problems and evaluating answers.
    """

    #Required fields for LMS
    has_score = True
    icon_class = "problem"

    # Fields for the author to define the problem and rubric
    problem_description = String(
        default="Is Linux FOSS?",
        scope=Scope.content,
        help="The description of the problem to be solved.",
        max_length=500  # Adjust max_length as needed
    )
    
    rubric = String(
        default="Determine whether the student has correctly answered the question. If so, reply with 'meets expectation', otherwise reply with 'does not meet expectation'. You must include one of those exact strings in your answer. Then, provide feedback to the student.",
        scope=Scope.content,
        help="The rubric for evaluating answers.",
        max_length=500  # Adjust max_length as needed
    )

    # Field for student answers
    student_answer = String(
        default="",
        scope=Scope.user_state,
        help="The student's answer to the problem."
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        return files(__package__).joinpath(path).read_text(encoding="utf-8")

    def phi_moe_api_text_text_endpoint(self,document_text: str, prompt_text: str, max_length: int) -> str:
        """
        Sends a request to the API endpoint and returns the response.

        Args:
        document_text (str): The document text to be processed.
        prompt_text (str): The prompt text to be used for processing.
        max_length (int): Maximum length of the generated text.

        Returns:
        str: The generated text from the API.
        """
        print("Hey, we're here")
        url = "http://ece-nebula16.eng.uwaterloo.ca:8000/generate"
        headers = {"Content-Type": "application/json"}
        data = {
        "prompt": f"{prompt_text}\n{document_text}",
        "max_length": max_length
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the JSON response
        response_json = response.json()['response']
        #generated_text = response_json.get("response", "").strip()

        return response_json

    def student_view(self, context=None):
        """
        The primary view of the ButtonXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/student_view.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/button.css"))
        frag.add_javascript(self.resource_string("static/js/src/button.js"))
        frag.initialize_js('ButtonXBlock')
        return frag

    # Author view
    def author_view(self, context=None):
        """
        The instructor view of the ButtonXBlock, allowing them to edit
        the problem description and rubric.
        """
        html = self.resource_string("static/html/student_view.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/button.css"))
        frag.add_javascript(self.resource_string("static/js/src/button.js"))
        frag.initialize_js('ButtonXBlock')
        return frag
        
    # Studio view
    def studio_view(self, context=None):
        """
        The instructor view of the ButtonXBlock, allowing them to edit
        the problem description and rubric.
        """
        html = self.resource_string("static/html/studio_view.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/button.css"))
        frag.add_javascript(self.resource_string("static/js/src/button.js"))
        frag.initialize_js('ButtonXBlock')
        return frag    

    @XBlock.json_handler
    def save_problem_and_rubric(self, data, suffix=''):
        """
        Save the problem description and rubric from the instructor.
        """
        self.problem_description = data.get('problem_description', '')
        self.rubric = data.get('rubric', '')
        return {"problem_description": self.problem_description, "rubric": self.rubric}
     

    @XBlock.json_handler
    def evaluate_answer(self, data, suffix=''):
        """
        Handler to evaluate the student's answer.
        """
        self.student_answer = data.get('answer', '')
        
        # Extract the rubric and problem description
        problem = self.problem_description
        rubric = self.rubric
        answer = self.student_answer
        
        # Call your evaluation function here
        # For example: result = evaluate_function(problem, rubric, answer)
        system = f"You are evaluating a student's answer to the question {problem}. Your evaluation criteria are: {rubric}. The student answer is: "
        print("We are evaluating")
        evaluation = self.phi_moe_api_text_text_endpoint(answer,system,max_length=256)#text_text_eval(answer, system,model='phi',max_length=256)
        
        #publish the score
        #if "meets expectation" in evaluation:
            #self.runtime.publish(self,"grade",{value:1.0, max_value: 1.0})
        #else:
            #self.runtime.publish(self,"grade",{value:0.0,max_value: 1.0})
    
        return {"problem": problem, "rubric": rubric, "answer": answer,"evaluation": evaluation}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ButtonXBlock",
             """<button/>
             """),
            ("Multiple ButtonXBlock",
             """<vertical_demo>
                <button/>
                <button/>
                <button/>
                </vertical_demo>
             """),
        ]

