candidate_schema = {
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
                    "description": "Key strengths of the candidate in this job interview",
                    "items": {"type": "string"}
                },
                "weaknesses": {
                    "type": "array",
                    "description": "Key weaknesses of the candidate in this job interview",
                    "items": {"type": "string"}
                },
                "opportunities": {
                    "type": "array",
                    "description": "Key opportunities that may come up for the candidate in this job role",
                    "items": {"type": "string"}
                },
                "threats": {
                    "type": "array",
                    "description": "Key threats that may come up for the candidate in this job role",
                    "items": {"type": "string"}
                }
            },
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
                    "yt_search_query": {
                        "type": "string",
                        "description": "Youtube search query to get videos to learn about this topic"
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
                            "required": ["question", "answer"]
                        }
                    }
                },
                "required": ["topic", "brief", "yt_search_query", "interview_questions"]
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
                "required": ["information_type", "info"]
            }
        }
    },
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
response_format_candidate = {

    "name": "interview_cheatsheet",
    "description": "Generates a cheatsheet for a job role",
    "strict": True,
    "schema":candidate_schema
}

interviewer_schema = {
  "type": "object",
  "properties": {
    "candidate_info": {
      "type": "object",
      "description": "Basic information about the candidate",
      "properties": {
        "name": {
          "type": "string",
          "description": "Full name of the candidate"
        },
        "contact": {
          "type": "object",
          "properties": {
            "email": {"type": "string"},
            "phone": {"type": "string"},
            "location": {"type": "string"}
          },
          "required": ["email"]
        },
        "current_role": {"type": "string"},
        "years_of_experience": {"type": "number"}
      },
      "required": ["name", "contact", "years_of_experience"]
    },
    "job_requirements": {
      "type": "object",
      "description": "Skills and qualifications required for the job",
      "properties": {
        "must_have_skills": {
          "type": "array",
          "description": "Skills that are essential for the role",
          "items": {
            "type": "object",
            "properties": {
              "skill_name": {"type": "string"},
              "candidate_proficiency": {
                "type": "number",
                "description": "Score (0-2): 0 = not demonstrated, 1 = listed in resume but not proven, 2 = proven in projects/experience. Be very strict here"
              },
              "evidence": {
                "type": "string",
                "description": "Supporting evidence from resume for the proficiency score"
              }
            },
            "required": ["skill_name", "candidate_proficiency"]
          }
        },
        "good_to_have_skills": {
          "type": "array",
          "description": "Skills that are beneficial but not mandatory",
          "items": {
            "type": "object",
            "properties": {
              "skill_name": {"type": "string"},
              "candidate_proficiency": {
                "type": "number",
                "description": "Score (0-2): 0 = not demonstrated, 1 = listed but not proven, 2 = proven in projects/experience"
              },
              "evidence": {
                "type": "string",
                "description": "Supporting evidence from resume for the proficiency score"
              }
            },
            "required": ["skill_name", "candidate_proficiency"]
          }
        }
      },
      "required": ["must_have_skills", "good_to_have_skills"]
    },
    "resume_analysis": {
      "type": "object",
      "description": "Automated analysis of the candidate's resume",
      "properties": {
        "education_match": {
          "type": "object",
          "properties": {
            "required_education": {"type": "string"},
            "candidate_education": {"type": "string"},
            "match_score": {
              "type": "number",
              "description": "Score from 0-10 indicating how well the candidate's education matches requirements"
            },
            "score_reasoning": {
              "type": "string",
              "description": "Detailed explanation for the education match score"
            },
            "notes": {"type": "string"}
          },
          "required": ["required_education", "candidate_education", "match_score", "score_reasoning"]
        },
        "experience_match": {
          "type": "object",
          "properties": {
            "required_years": {"type": "number"},
            "candidate_years": {"type": "number"},
            "relevant_experience_score": {
              "type": "number",
              "description": "Score from 0-10 on relevance of experience, not just years"
            },
            "score_reasoning": {
              "type": "string",
              "description": "Detailed explanation for the experience relevance score"
            },
            "notes": {"type": "string"}
          },
          "required": ["required_years", "candidate_years", "relevant_experience_score", "score_reasoning"]
        },
        "skill_gaps": {
          "type": "array",
          "description": "Critical skills from job description that appear to be missing in resume",
          "items": {"type": "string"}
        },
        "keyword_match_score": {
          "type": "number",
          "description": "Percentage of key job description terms found in resume"
        },
        "keyword_match_reasoning": {
          "type": "string",
          "description": "Explanation of keyword match analysis and significance"
        }
      },
      "required": ["education_match", "experience_match", "skill_gaps", "keyword_match_score", "keyword_match_reasoning"]
    },
    "screening_questions": {
      "type": "array",
      "description": "Pre-interview questions to validate resume claims and assess fit",
      "items": {
        "type": "object",
        "properties": {
          "question": {"type": "string"},
          "expected_response": {
            "type": "string",
            "description": "Indicators of a strong response"
          },
          "importance": {
            "type": "string",
            "enum": ["high", "medium", "low"]
          },
          "skills_validated": {
            "type": "array",
            "description": "Skills being validated through this question",
            "items": {"type": "string"}
          }
        },
        "required": ["question", "expected_response", "importance", "skills_validated"]
      }
    },
    "preliminary_assessment": {
      "type": "object",
      "description": "Initial assessment based on resume review",
      "properties": {
        "technical_fit_score": {
          "type": "number",
          "description": "Score from 0-10 on technical qualifications"
        },
        "technical_fit_reasoning": {
          "type": "string",
          "description": "Detailed explanation for the technical fit score"
        },
        "experience_fit_score": {
          "type": "number",
          "description": "Score from 0-10 on experience alignment"
        },
        "experience_fit_reasoning": {
          "type": "string",
          "description": "Detailed explanation for the experience fit score"
        },
        "potential_culture_fit": {
          "type": "number",
          "description": "Score from 0-10 based on resume indicators"
        },
        "culture_fit_reasoning": {
          "type": "string",
          "description": "Explanation of culture fit indicators from resume"
        },
        "salary_expectations": {
          "type": "object",
          "properties": {
            "range_min": {"type": "number"},
            "range_max": {"type": "number"},
            "within_budget": {"type": "boolean"},
            "notes": {"type": "string"}
          }
        },
        "strengths": {
          "type": "array",
          "description": "Notable strengths that align well with the role",
          "items": {"type": "string"}
        }
      },
      "required": [
        "technical_fit_score",
        "technical_fit_reasoning",
        "experience_fit_score",
        "experience_fit_reasoning",
        "potential_culture_fit",
        "culture_fit_reasoning"
      ]
    },
    "screening_decision": {
      "type": "object",
      "properties": {
        "decision_reasoning": {
          "type": "string",
          "description": "Explanation for the interview decision"
        },
        "interview_type": {
          "type": "string",
          "enum": ["technical", "behavioral", "comprehensive"]
        },
        "interviewer_recommendations": {
          "type": "array",
          "description": "Team members who should be involved in the interview",
          "items": {
            "type": "object",
            "properties": {
              "role": {"type": "string"},
              "reason": {"type": "string"},
              "skill_areas_to_assess": {
                "type": "array",
                "items": {"type": "string"}
              }
            },
            "required": ["role", "skill_areas_to_assess"]
          }
        },
        "priority": {
          "type": "string",
          "enum": ["high", "medium", "low"],
          "description": "How quickly to schedule the interview"
        },
        "priority_justification": {
          "type": "string",
          "description": "Explanation for the assigned priority level"
        },
        "additional_preparation": {
          "type": "array",
          "description": "Additional information to gather before interview",
          "items": {"type": "string"}
        }
      },
      "required": ["decision_reasoning", "interview_type", "priority", "priority_justification"]
    },
    "compliance_check": {
      "type": "object",
      "description": "Ensuring unbiased and compliant screening process",
      "properties": {
        "bias_indicators": {
          "type": "array",
          "description": "Potential bias elements to be aware of",
          "items": {"type": "string"}
        },
        "accommodations_needed": {
          "type": "boolean",
          "description": "Whether candidate has requested accommodations"
        },
        "diversity_initiative_alignment": {
          "type": "boolean",
          "description": "Whether candidate helps meet diversity goals"
        }
      },
      "required": ["bias_indicators"]
    }
  },
  "required": [
    "candidate_info",
    "job_requirements",
    "resume_analysis",
    "preliminary_assessment",
    "screening_decision"
  ]
}

response_format_interviewer = {

    "name": "interview_cheatsheet",
    "description": "Generates a cheatsheet for a job role",
    "strict": True,
    "schema":interviewer_schema
}



jd_summary_schema = {
  "type": "object",
  "properties": {
    "job_metadata": {
      "type": "object",
      "description": "Essential job information",
      "properties": {
        "job_name": {"type": "string", "description": "Title of the position"},
        "company_name": {"type": "string", "description": "Name of the hiring company"},
        "location": {"type": "string"},
        "employment_type": {
          "type": "string",
          "enum": ["full_time", "part_time", "contract", "internship"]
        },
        "seniority_level": {
          "type": "string",
          "enum": ["entry", "mid_level", "senior", "executive"]
        }
      },
      "required": ["job_name", "company_name"]
    },
    "compensation": {
      "type": "object",
      "properties": {
        "salary_range": {
          "type": "object",
          "properties": {
            "min": {"type": "number"},
            "max": {"type": "number"},
            "currency": {"type": "string"}
          }
        },
        "benefits": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    },
    "job_requirements": {
      "type": "object",
      "description": "Key requirements for the position",
      "properties": {
        "must_have_skills": {
          "type": "array",
          "description": "Essential skills for the role",
          "items": {
            "type": "object",
            "properties": {
              "skill_name": {"type": "string"},
              "years_experience_required": {"type": "number"}
            },
            "required": ["skill_name"]
          }
        },
        "good_to_have_skills": {
          "type": "array",
          "items": {"type": "string"}
        },
        "education": {
          "type": "object",
          "properties": {
            "minimum_level": {
              "type": "string",
              "enum": ["high_school", "bachelor", "master", "phd"]
            },
            "preferred_fields": {"type": "array", "items": {"type": "string"}}
          }
        },
        "experience": {
          "type": "object",
          "properties": {
            "minimum_years": {"type": "number"},
            "preferred_years": {"type": "number"}
          },
          "required": ["minimum_years"]
        }
      },
      "required": ["must_have_skills", "experience"]
    },
    "job_responsibilities": {
      "type": "object",
      "description": "Primary duties of the role",
      "properties": {
        "primary_duties": {
          "type": "array",
          "items": {"type": "string"}
        },
        "management_responsibilities": {
          "type": "object",
          "properties": {
            "has_direct_reports": {"type": "boolean"},
            "team_size": {"type": "number"}
          }
        }
      },
      "required": ["primary_duties"]
    },
    "company_profile": {
      "type": "object",
      "properties": {
        "industry": {"type": "string"},
        "company_size": {
          "type": "string",
          "enum": ["small", "medium", "large", "enterprise"]
        }
      }
    },
    "keywords": {
      "type": "array",
      "description": "Essential keywords from the job description",
      "items": {
        "type": "object",
        "properties": {
          "term": {"type": "string"},
          "importance": {
            "type": "string",
            "enum": ["critical", "high", "medium", "low"]
          }
        },
        "required": ["term"]
      }
    },
    "job_summary": {
      "type": "string",
      "description": "Concise summary of the key aspects of the job"
    }
  },
  "required": [
    "job_metadata",
    "job_requirements",
    "job_responsibilities",
    "keywords",
    "job_summary"
  ]
}

response_format_jd_summary = {

    "name": "interview_cheatsheet",
    "description": "Generates a cheatsheet for a job role",
    "strict": True,
    "schema":jd_summary_schema
}