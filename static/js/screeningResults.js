// Helper function to set score bar
function setScoreBar(elementId, score, isPercentage = false) {
  const element = document.getElementById(elementId);
  const scoreElement = document.getElementById(`${elementId}-score`);
  
  if (!element || !scoreElement) return;
  
  const value = isPercentage ? score : score * 10;
  let color;
  
  if (score >= 8 || (isPercentage && score >= 80)) {
    color = 'var(--success-color)';
  } else if (score >= 6 || (isPercentage && score >= 60)) {
    color = 'var(--warning-color)';
  } else {
    color = 'var(--danger-color)';
  }
  
  // Create and append a span for the colored part
  const coloredPart = document.createElement('span');
  coloredPart.style.position = 'absolute';
  coloredPart.style.left = '0';
  coloredPart.style.top = '0';
  coloredPart.style.height = '100%';
  coloredPart.style.width = `${value}%`;
  coloredPart.style.backgroundColor = color;
  coloredPart.style.borderRadius = '9999px';
  
  // Clear any existing colored parts
  while (element.firstChild) {
    element.removeChild(element.firstChild);
  }
  
  element.appendChild(coloredPart);
  
  // Set the score text
  scoreElement.textContent = isPercentage ? `${score}%` : `${score}/10`;
}

// Helper function to create list items
function createListItems(elementId, items) {
  const element = document.getElementById(elementId);
  if (!element) return;
  
  element.innerHTML = '';
  
  if (!items || items.length === 0) {
    const li = document.createElement('li');
    li.textContent = 'None';
    element.appendChild(li);
    return;
  }
  
  items.forEach(item => {
    const li = document.createElement('li');
    li.textContent = typeof item === 'string' ? item : item.concern || item;
    element.appendChild(li);
  });
}

// Helper function to create skill badges
function createSkillBadges(elementId, skills) {
  const element = document.getElementById(elementId);
  if (!element) return;
  
  element.innerHTML = '';
  
  if (!skills || skills.length === 0) {
    const emptyMessage = document.createElement('p');
    emptyMessage.textContent = 'None specified';
    emptyMessage.style.color = 'var(--gray-500)';
    emptyMessage.style.fontSize = '0.875rem';
    element.appendChild(emptyMessage);
    return;
  }
  
  skills.forEach(skill => {
    const badge = document.createElement('div');
    badge.className = 'skill-badge';
    
    const name = document.createElement('span');
    name.textContent = skill.skill_name;
    
    badge.appendChild(name);
    
    if (typeof skill.candidate_proficiency !== 'undefined') {
      const score = document.createElement('span');
      score.className = `skill-score skill-score-${skill.candidate_proficiency}`;
      score.textContent = skill.candidate_proficiency;
      badge.appendChild(score);
      
      // Add tooltip with evidence if available
      if (skill.evidence && skill.evidence !== 'null') {
        badge.title = `Evidence: ${skill.evidence}`;
      }
    }
    
    element.appendChild(badge);
  });
}

// Helper function to create interviewer cards
function createInterviewerCards(elementId, interviewers) {
  const element = document.getElementById(elementId);
  if (!element) return;
  
  element.innerHTML = '';
  
  if (!interviewers || interviewers.length === 0) {
    const emptyMessage = document.createElement('p');
    emptyMessage.textContent = 'No specific interviewers recommended';
    emptyMessage.style.color = 'var(--gray-500)';
    emptyMessage.style.fontSize = '0.875rem';
    element.appendChild(emptyMessage);
    return;
  }
  
  interviewers.forEach(interviewer => {
    const card = document.createElement('div');
    card.className = 'interviewer-card';
    
    const role = document.createElement('p');
    role.className = 'interviewer-role';
    role.textContent = interviewer.role;
    
    const reason = document.createElement('p');
    reason.className = 'interviewer-reason';
    reason.textContent = interviewer.reason || '';
    
    card.appendChild(role);
    card.appendChild(reason);
    
    // Add skills to assess if available
    if (interviewer.skill_areas_to_assess && interviewer.skill_areas_to_assess.length > 0) {
      const skillsContainer = document.createElement('div');
      skillsContainer.className = 'interviewer-skills';
      
      interviewer.skill_areas_to_assess.forEach(skill => {
        const skillBadge = document.createElement('span');
        skillBadge.className = 'interviewer-skill';
        skillBadge.textContent = skill;
        skillsContainer.appendChild(skillBadge);
      });
      
      card.appendChild(skillsContainer);
    }
    
    element.appendChild(card);
  });
}

// Helper function to create screening questions
function createScreeningQuestions(elementId, questions) {
  const element = document.getElementById(elementId);
  if (!element) return;
  
  element.innerHTML = '';
  
  if (!questions || questions.length === 0) {
    const emptyMessage = document.createElement('p');
    emptyMessage.textContent = 'No screening questions recommended';
    emptyMessage.style.color = 'var(--gray-500)';
    emptyMessage.style.fontSize = '0.875rem';
    element.appendChild(emptyMessage);
    return;
  }
  
  questions.forEach(question => {
    const questionDiv = document.createElement('div');
    questionDiv.className = 'question';
    
    const importance = document.createElement('span');
    importance.className = `question-importance ${question.importance}`;
    importance.textContent = question.importance;
    
    const questionText = document.createElement('p');
    questionText.className = 'question-text';
    questionText.textContent = question.question;
    
    const expected = document.createElement('p');
    expected.className = 'question-expected';
    
    const expectedLabel = document.createElement('span');
    expectedLabel.textContent = 'Expected: ';
    
    expected.appendChild(expectedLabel);
    expected.appendChild(document.createTextNode(question.expected_response));
    
    questionDiv.appendChild(importance);
    questionDiv.appendChild(questionText);
    questionDiv.appendChild(expected);
    
    // Add skills validated if available
    if (question.skills_validated && question.skills_validated.length > 0) {
      const skillsContainer = document.createElement('div');
      skillsContainer.className = 'question-skills';
      
      question.skills_validated.forEach(skill => {
        const skillBadge = document.createElement('span');
        skillBadge.className = 'question-skill';
        skillBadge.textContent = skill;
        skillsContainer.appendChild(skillBadge);
      });
      
      questionDiv.appendChild(skillsContainer);
    }
    
    element.appendChild(questionDiv);
  });
}

// Helper function to set text content
function setText(elementId, text) {
  const element = document.getElementById(elementId);
  if (element) {
    element.textContent = text || 'Not specified';
  }
}

// Helper function to set HTML content
function setHTML(elementId, html) {
  const element = document.getElementById(elementId);
  if (element) {
    element.innerHTML = html || '';
  }
}

// Function to calculate the total match percentage
function calculateTotalMatchPercentage(candidateData) {
  const { 
    preliminary_assessment, 
    resume_analysis
  } = candidateData;
  
  // Calculate weighted average of different scores
  const technicalWeight = 0.5;
  const experienceWeight = 0.3;
  const cultureWeight = 0.1;
  const educationWeight = 0.1;
  const keywordWeight = 0.0;
  
  const technicalScore = preliminary_assessment.technical_fit_score * 10; // Scale to 0-100
  const experienceScore = preliminary_assessment.experience_fit_score * 10;
  const cultureScore = preliminary_assessment.potential_culture_fit * 10;
  const educationScore = resume_analysis.education_match.match_score * 10;
  const keywordScore = resume_analysis.keyword_match_score; // Already 0-100
  
  const totalScore = 
    (technicalScore * technicalWeight) +
    (experienceScore * experienceWeight) +
    (cultureScore * cultureWeight) +
    (educationScore * educationWeight) +
    (keywordScore * keywordWeight);
  
  return Math.round(totalScore);
}

// Function to draw the must-have skills radar chart
function drawMustHaveSkillsRadarChart(containerId, skills) {
  const canvas = document.getElementById(containerId);
  if (!canvas || !skills || skills.length === 0) return;
  
  const ctx = canvas.getContext('2d');
  const width = canvas.width = canvas.offsetWidth;
  const height = canvas.height = canvas.offsetHeight;
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(centerX, centerY) * 0.8;
  
  // Clear canvas
  ctx.clearRect(0, 0, width, height);
  
  const numSkills = skills.length;
  const angleStep = (Math.PI * 2) / numSkills;
  
  // Draw concentric circles
  const levels = 3; // 5 levels (0-10 score with step 2)
  for (let level = 1; level <= levels; level++) {
    const levelRadius = (radius / levels) * level;
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, levelRadius, 0, Math.PI * 2);
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth = 1;
    ctx.stroke();
    
    // Add score label for this level
    if (level < levels) {
      const score = level.toString();
      ctx.fillStyle = '#9ca3af';
      ctx.font = '10px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(score, centerX, centerY - levelRadius);
    }
  }
  
  // Draw axis lines and labels
  for (let i = 0; i < numSkills; i++) {
    const angle = i * angleStep - Math.PI / 2; // Start from top (subtract 90 degrees)
    const x = centerX + radius * Math.cos(angle);
    const y = centerY + radius * Math.sin(angle);
    
    // Draw axis line
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(x, y);
    ctx.strokeStyle = '#d1d5db';
    ctx.lineWidth = 1;
    ctx.stroke();
    
    // Draw axis label
    const labelX = centerX + (radius + 20) * Math.cos(angle);
    const labelY = centerY + (radius + 20) * Math.sin(angle);
    
    ctx.fillStyle = '#4b5563';
    ctx.font = 'bold 12px sans-serif';
    
    // Adjust text alignment based on position
    if (Math.abs(angle - Math.PI / 2) < 0.1 || Math.abs(angle + Math.PI / 2) < 0.1) {
      // Top or bottom
      ctx.textAlign = 'center';
    } else if (angle < 0 || angle > Math.PI) {
      // Right side
      ctx.textAlign = 'left';
    } else {
      // Left side
      ctx.textAlign = 'right';
    }
    
    ctx.fillText(skills[i].skill_name, labelX, labelY);
  }
  
  // Draw data points and connect them
  ctx.beginPath();
  
  for (let i = 0; i < numSkills; i++) {
    const angle = i * angleStep - Math.PI / 2; // Start from top
    const score = skills[i].candidate_proficiency || 0;
    const pointRadius = (radius / (levels-1)) * score; // Scale to fit within the chart (max score is 5)
    
    const x = centerX + pointRadius * Math.cos(angle);
    const y = centerY + pointRadius * Math.sin(angle);
    
    if (i === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  }
  
  // Close the path
  const firstAngle = -Math.PI / 2; // Start from top
  const firstScore = skills[0].candidate_proficiency || 0;
  const firstX = centerX + (radius / (levels-1)) * firstScore * Math.cos(firstAngle);
  const firstY = centerY + (radius / (levels-1)) * firstScore * Math.sin(firstAngle);
  ctx.lineTo(firstX, firstY);
  
  // Fill with semi-transparent color
  ctx.fillStyle = 'rgba(74, 108, 247, 0.2)';
  ctx.fill();
  
  // Stroke the outline
  ctx.strokeStyle = 'rgba(74, 108, 247, 0.8)';
  ctx.lineWidth = 2;
  ctx.stroke();
  
  // Draw data points
  for (let i = 0; i < numSkills; i++) {
    const angle = i * angleStep - Math.PI / 2;
    const score = skills[i].candidate_proficiency || 0;
    const pointRadius = (radius / (levels-1)) * score;
    
    const x = centerX + pointRadius * Math.cos(angle);
    const y = centerY + pointRadius * Math.sin(angle);
    
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(74, 108, 247, 1)';
    ctx.fill();
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 1;
    ctx.stroke();
    
    // Add score label
    ctx.fillStyle = '#1f2937';
    ctx.font = 'bold 12px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText((score+1).toString(), x, y);
  }
}

// Function to create and add the total match percentage to the header
function addTotalMatchPercentage(candidateData) {
  const matchPercentage = calculateTotalMatchPercentage(candidateData);
  
  // Create the match percentage element
  const matchContainer = document.createElement('div');
  matchContainer.className = 'total-match-container';
  
  const matchLabel = document.createElement('span');
  matchLabel.textContent = 'Candidate score:';
  matchLabel.className = 'total-match-label';
  
  const matchValue = document.createElement('span');
  matchValue.textContent = `${matchPercentage}%`;
  matchValue.className = 'total-match-value';
  
  // Set color based on match percentage
  if (matchPercentage >= 80) {
    matchValue.style.color = 'var(--success-color)';
  } else if (matchPercentage >= 60) {
    matchValue.style.color = 'var(--warning-color)';
  } else {
    matchValue.style.color = 'var(--danger-color)';
  }
  
  matchContainer.appendChild(matchLabel);
  matchContainer.appendChild(matchValue);
  
  // Add to the header
  const headerContent = document.querySelector('.header-content');
  const decisionInfo = document.querySelector('.decision-info');
  
  if (headerContent && decisionInfo) {
    headerContent.insertBefore(matchContainer, decisionInfo);
  }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
  const { 
    candidate_info, 
    preliminary_assessment, 
    resume_analysis, 
    screening_decision,
    compliance_check,
    screening_questions,
    job_requirements
  } = candidateData;
  
  // Add total match percentage to header
  addTotalMatchPercentage(candidateData);
  
  // Set candidate info
  setText('candidate-name', candidate_info.name);
  setText('current-role', candidate_info.current_role && candidate_info.current_role !== 'null' ? 
    `💼 ${candidate_info.current_role}` : '💼 No current role');
  setText('email', `📧 ${candidate_info.contact.email}`);
  setText('phone', `📱 ${candidate_info.contact.phone}`);
  if (candidate_info.contact.location) {
    setText('location', `📍 ${candidate_info.contact.location}`);
  }
  
  // Set years of experience
  setText('years-experience', `${candidate_info.years_of_experience} years`);
  
  // Set interview type
  const interviewTypeContainer = document.getElementById('interview-type-container');
  if (interviewTypeContainer) {
    const interviewType = document.createElement('div');
    interviewType.className = 'badge';
    interviewType.textContent = `${screening_decision.interview_type.charAt(0).toUpperCase() + screening_decision.interview_type.slice(1)} Interview`;
    interviewType.style.backgroundColor = '#dbeafe';
    interviewType.style.color = '#1e40af';
    interviewTypeContainer.appendChild(interviewType);
  }
  
  // Set priority badge
  const priorityBadge = document.getElementById('priority-badge');
  if (priorityBadge) {
    priorityBadge.textContent = screening_decision.priority;
    
    if (screening_decision.priority === 'high') {
      priorityBadge.style.backgroundColor = '#fee2e2';
      priorityBadge.style.color = '#991b1b';
    } else if (screening_decision.priority === 'medium') {
      priorityBadge.style.backgroundColor = '#fef3c7';
      priorityBadge.style.color = '#92400e';
    } else {
      priorityBadge.style.backgroundColor = '#dbeafe';
      priorityBadge.style.color = '#1e40af';
    }
  }
  
  // Replace radar chart with must-have and good-to-have skills radar charts
  const radarContainer = document.querySelector('.radar-chart-container');
  if (radarContainer) {
    radarContainer.innerHTML = '';
    
    // Create title for Must-Have Skills radar
    const mustHaveTitle = document.createElement('h4');
    mustHaveTitle.textContent = 'Must-Have Skills';
    mustHaveTitle.style.textAlign = 'center';
    mustHaveTitle.style.marginBottom = '8px';
    radarContainer.appendChild(mustHaveTitle);
    
    // Create canvas for Must-Have Skills radar
    const mustHaveCanvas = document.createElement('canvas');
    mustHaveCanvas.id = 'must-have-radar';
    mustHaveCanvas.style.width = '100%';
    mustHaveCanvas.style.height = '250px';
    radarContainer.appendChild(mustHaveCanvas);
    
    // Create title for Good-to-Have Skills radar (if there are any)
    if (job_requirements.good_to_have_skills && job_requirements.good_to_have_skills.length > 0) {
      const goodToHaveTitle = document.createElement('h4');
      goodToHaveTitle.textContent = 'Good-to-Have Skills';
      goodToHaveTitle.style.textAlign = 'center';
      goodToHaveTitle.style.marginTop = '24px';
      goodToHaveTitle.style.marginBottom = '8px';
      radarContainer.appendChild(goodToHaveTitle);
      
      // Create canvas for Good-to-Have Skills radar
      const goodToHaveCanvas = document.createElement('canvas');
      goodToHaveCanvas.id = 'good-to-have-radar';
      goodToHaveCanvas.style.width = '100%';
      goodToHaveCanvas.style.height = '250px';
      radarContainer.appendChild(goodToHaveCanvas);
    }
  }
  
  // Set assessment scores
  setScoreBar('technical-fit', preliminary_assessment.technical_fit_score);
  setScoreBar('experience-fit', preliminary_assessment.experience_fit_score);
  setScoreBar('culture-fit', preliminary_assessment.potential_culture_fit);
  
  // Set education & experience
  setText('education', resume_analysis.education_match.candidate_education);
  setScoreBar('education-match', resume_analysis.education_match.match_score);
  setText('education-score-reasoning', resume_analysis.education_match.score_reasoning || resume_analysis.education_match.notes);
  
  setText('experience', `${candidate_info.years_of_experience} years (Required: ${resume_analysis.experience_match.required_years} years)`);
  setScoreBar('experience-match', resume_analysis.experience_match.relevant_experience_score);
  setText('experience-score-reasoning', resume_analysis.experience_match.score_reasoning || resume_analysis.experience_match.notes);
  
  // Set keyword match
  setScoreBar('keyword-match', resume_analysis.keyword_match_score, true);
  setText('keyword-match-reasoning', resume_analysis.keyword_match_reasoning);
  
  // Set strengths & gaps
  createListItems('strengths', preliminary_assessment.strengths);
  createListItems('skill-gaps', resume_analysis.skill_gaps);
  
  // Set skills
  createSkillBadges('must-have-skills', job_requirements.must_have_skills);
  createSkillBadges('good-to-have-skills', job_requirements.good_to_have_skills);
  
  // Set compliance check
  const biasIndicatorsContainer = document.getElementById('bias-indicators-container');
  if (biasIndicatorsContainer) {
    if (!compliance_check.bias_indicators || compliance_check.bias_indicators.length === 0) {
      biasIndicatorsContainer.innerHTML = '<p style="color: var(--success-color);">No bias indicators detected</p>';
    } else {
      const ul = document.createElement('ul');
      ul.className = 'list';
      compliance_check.bias_indicators.forEach(indicator => {
        const li = document.createElement('li');
        li.textContent = indicator;
        ul.appendChild(li);
      });
      biasIndicatorsContainer.appendChild(ul);
    }
  }
  
  setText('accommodations', compliance_check.accommodations_needed ? 'Yes' : 'No');
  setText('diversity', compliance_check.diversity_initiative_alignment ? 'Yes' : 'No');
  
  // Set interview recommendations
  setText('decision-reasoning', screening_decision.decision_reasoning);
  setText('priority-justification', screening_decision.priority_justification);
  createListItems('additional-preparation', screening_decision.additional_preparation);
  createInterviewerCards('interviewers', screening_decision.interviewer_recommendations);
  
  // Set screening questions
  createScreeningQuestions('screening-questions', screening_questions);
  
  // Set current date
  setText('current-date', new Date().toLocaleDateString());
  
  // Draw the skills radar charts
  drawMustHaveSkillsRadarChart('must-have-radar', job_requirements.must_have_skills);
  if (job_requirements.good_to_have_skills && job_requirements.good_to_have_skills.length > 0) {
    drawMustHaveSkillsRadarChart('good-to-have-radar', job_requirements.good_to_have_skills);
  }
  
  // Handle window resize for radar charts
  window.addEventListener('resize', function() {
    drawMustHaveSkillsRadarChart('must-have-radar', job_requirements.must_have_skills);
    if (job_requirements.good_to_have_skills && job_requirements.good_to_have_skills.length > 0) {
      drawMustHaveSkillsRadarChart('good-to-have-radar', job_requirements.good_to_have_skills);
    }
  });
});