response_format = {
    "name": "interview_cheatsheet",
    "description": "Generates a cheatsheet for a job role",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "company": {
                "type": "string",
                "description": "The company that the job description belongs to"
            },
            "role": {
                "type": "string",
                "description": "The role that the job description belongs to"
            },
            "swot_analysis": {
                "type": "object",
                "description": "A SWOT analysis of the candidate for this particular job role in terms of experience, skillsets, and culture match",
                "properties": {
                    "strengths": {
                        "type": "array",
                        "description": "Key strengths of the candidate for the role",
                        "items": {"type": "string"}
                    },
                    "weaknesses": {
                        "type": "array",
                        "description": "Key weaknesses of the candidate for this role",
                        "items": {"type": "string"}
                    },
                    "opportunities": {
                        "type": "array",
                        "description": "Key opportunities for the candidate in this role",
                        "items": {"type": "string"}
                    },
                    "threats": {
                        "type": "array",
                        "description": "Key threats for the candidate in this role",
                        "items": {"type": "string"}
                    }
                },
                "additionalProperties": False,
                "required": ["strengths", "weaknesses", "opportunities", "threats"]
            },
            "requiredskills": {
                "type": "array",
                "description": "A list of skills required for the role",
                "items": {
                    "type": "object",
                    "properties": {
                        "skill": {"type": "string"},
                        "candidate_skill": {
                            "type": "boolean",
                            "description": "Based on the resume, does the candidate have the skill or not?"
                        }
                    },
                    "additionalProperties": False,
                    "required": ["skill", "candidate_skill"]
                }
            },
            "concepts_revision": {
                "type": "array",
                "description": "Topics that could be covered in the interview, based on the job description. Be exhaustive and cover all topics mentioned in the job description",
                "items": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string"},
                        "brief": {
                            "type": "string",
                            "description": "An introduction about what the topic is, why it's relevant to the role, and how the candidate can prepare for it"
                        },
                        "youtube_video": {
                            "type": "string",
                            "description": "Title of a YouTube video that summarizes this topic"
                        },
                        "interview_questions": {
                            "type": "array",
                            "description": "Questions that can come up during the interview on this topic. Include at least 4.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "question": {
                                        "type": "string",
                                        "description": "A question on this topic relevant to the role"
                                    },
                                    "answer": {
                                        "type": "string",
                                        "description": "Answer for the question"
                                    }
                                },
                                "additionalProperties": False,
                                "required": ["question", "answer"]
                            }
                        }
                    },
                    "additionalProperties": False,
                    "required": ["topic", "brief", "youtube_video", "interview_questions"]
                }
            },
            "QA": {
                "type": "array",
                "description": "Questions that can come up during the interview based on the projects done and/or relevant to the job role. Include at least 10.",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "A question deep-diving into project specifics"
                        },
                        "answer": {
                            "type": "string",
                            "description": "Suggested or example answer for the question"
                        }
                    },
                    "additionalProperties": False,
                    "required": ["question", "answer"]
                }
            },
            "company_insights": {
                "type": "array",
                "description": "Insights about the company that might be useful during the interview, such as industry, business model, founding year, employee count, user base, annual revenue, headquarters, company values, and competitors. Add as much information about the company as possible. Be exhaustive.",
                "items": {
                    "type": "object",
                    "properties": {
                        "information_type": {
                            "type": "string",
                            "description": "The type of information, formatted neatly (e.g., 'Industry', 'Business Model')"
                        },
                        "info": {
                            "type": "string",
                            "description": "The information specific to the company. Make it concise (e.g., 'Technology', 'Subscription-based SaaS')."
                        }
                    },
                    "additionalProperties": False,
                    "required": ["information_type", "info"]
                }
            }
        },
        "additionalProperties": False,
        "required": [
            "company",
            "role",
            "swot_analysis",
            "requiredskills",
            "concepts_revision",
            "QA",
            "company_insights"
        ]
    }
}
