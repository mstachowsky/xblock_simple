import json
from xblock.core import XBlock
from xblock.fields import String, Scope
from web_fragments.fragment import Fragment
from importlib.resources import files
import requests

class ButtonXBlock(XBlock):
    """
    XBlock for writing problems and evaluating answers.
    """

    # Fields for the author to define the problem and rubric
    problem_description = String(
        default="Is Linux FOSS?",
        scope=Scope.content,
        help="The description of the problem to be solved.",
        max_length=500
    )
    
    rubric = String(
        default=json.dumps([
            {"label": "Meets Expectations", "text": ""},
            {"label": "Does Not Meet Expectations", "text": ""}
        ]),
        scope=Scope.content,
        help="The rubric for evaluating answers, stored as a JSON string.",
    )

    student_answer = String(
        default="",
        scope=Scope.user_state,
        help="The student's answer to the problem."
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        return files(__package__).joinpath(path).read_text(encoding="utf-8")

    def student_view(self, context=None):
        """The primary view of the ButtonXBlock, shown to students."""
        html = self.resource_string("static/html/student_view.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/button.css"))
        frag.add_javascript(self.resource_string("static/js/src/button.js"))
        frag.initialize_js('ButtonXBlock')
        return frag

    def studio_view(self, context=None):
        """The instructor view of the ButtonXBlock, allowing them to edit the problem description and rubric."""
        html = self.resource_string("static/html/studio_view.html")
        # Load the rubric from the JSON field
        rubric_data = json.loads(self.rubric)
        frag = Fragment(html.format(self=self, rubric_data=rubric_data))
        frag.add_css(self.resource_string("static/css/button.css"))
        frag.add_javascript(self.resource_string("static/js/src/button.js"))
        frag.initialize_js('ButtonXBlock')
        return frag    

    @XBlock.json_handler
    def save_problem_and_rubric(self, data, suffix=''):
        """Save the problem description and rubric from the instructor."""
        self.problem_description = data.get('problem_description', '')

        # Store the rubric as JSON
        rubric_sections = data.get('rubric_sections', [])
        self.rubric = json.dumps(rubric_sections)
        print(self.rubric)
        return {
            "problem_description": self.problem_description,
            "rubric": self.rubric
        }

    @XBlock.json_handler
    def evaluate_answer(self, data, suffix=''):
        """Handler to evaluate the student's answer."""
        self.student_answer = data.get('answer', '')
        problem = self.problem_description
        rubric = self.rubric
        answer = self.student_answer
        
        system = f"You are evaluating a student's answer to the question {problem}. Your evaluation criteria are: {rubric}. Evaluate the student answer and provide feedback. Your feedback must include exactly one of the criteria strings, then actionable feedback based only on the student answer and the criterion you chose. Do not make anything up, and do not make up extra criteria to evaluate the work against - if it isn't asked for, it is not needed. The student answer is: "
        evaluation = self.phi_moe_api_text_text_endpoint(answer, system, max_length=256)
        
        return {"problem": problem, "rubric": rubric, "answer": answer, "evaluation": evaluation}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ButtonXBlock", "<button/>"),
            ("Multiple ButtonXBlock", "<vertical_demo><button/><button/><button/></vertical_demo>"),
        ]

