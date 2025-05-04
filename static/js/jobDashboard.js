//import html2pdf from './html2pdf.js/dist/html2pdf.bundle.min.js';

function generateHTML(data) {
    return `
        <header class="job-header">
            <div class="company-info">
                <h1>${data.job_metadata.job_name}</h1>
                <h2>${data.job_metadata.company_name}</h2>
            </div>
            <div class="job-meta">
                <span class="badge">${data.job_metadata.employment_type.replace('_', ' ').toUpperCase()}</span>
                <span class="badge">${data.job_metadata.seniority_level.toUpperCase()}</span>
            </div>
        </header>

        <main class="job-content">
            <section class="job-summary">
                <h3>Job Summary</h3>
                <p>${data.job_summary}</p>
            </section>

            <div class="two-column">
                <section class="requirements">
                    <h3>Requirements</h3>
                    <div class="requirement-group">
                        <h4>Experience</h4>
                        <p>Minimum: ${data.job_requirements.experience.minimum_years} years</p>
                        <p>Preferred: ${data.job_requirements.experience.preferred_years} years</p>
                    </div>

                    <div class="requirement-group">
                        <h4>Must Have Skills</h4>
                        <ul class="skills-list">
                            ${data.job_requirements.must_have_skills.map(skill =>
                                `<li>${skill.skill_name} (${skill.years_experience_required} years)</li>`
                            ).join('')}
                        </ul>
                    </div>

                    <div class="requirement-group">
                        <h4>Education</h4>
                        <p>Minimum: ${data.job_requirements.education.minimum_level.charAt(0).toUpperCase() +
                                    data.job_requirements.education.minimum_level.slice(1)}'s degree</p>
                        <p>Preferred fields:</p>
                        <ul>
                            ${data.job_requirements.education.preferred_fields.map(field =>
                                `<li>${field}</li>`
                            ).join('')}
                        </ul>
                    </div>
                </section>

                <section class="responsibilities">
                    <h3>Responsibilities</h3>
                    <ul>
                        ${data.job_responsibilities.primary_duties.map(duty =>
                            `<li>${duty}</li>`
                        ).join('')}
                    </ul>

                    <div class="keywords">
                        <h4>Key Focus Areas</h4>
                        <div class="tags">
                            ${data.keywords.map(keyword =>
                                `<span class="tag ${keyword.importance}">${keyword.term}</span>`
                            ).join('')}
                        </div>
                    </div>
                </section>
            </div>

            <section class="benefits">
                <h3>Benefits</h3>
                <div class="benefits-grid">
                    ${data.compensation.benefits.map(benefit =>
                        `<div class="benefit-item">${benefit}</div>`
                    ).join('')}
                </div>
            </section>

            <section class="company-profile">
                <h3>About ${data.job_metadata.company_name}</h3>
                <div class="company-details">
                    <p><strong>Industry:</strong> ${data.company_profile.industry}</p>
                    <p><strong>Company Size:</strong> ${data.company_profile.company_size.charAt(0).toUpperCase() +
                                                     data.company_profile.company_size.slice(1)}</p>
                </div>
            </section>
        </main>
    `;
}

// Initialize the page
document.getElementById('jobContent').innerHTML = generateHTML(jobData);

// Setup PDF download
document.getElementById('downloadPdf').addEventListener('click', () => {
    const element = document.getElementById('jobContent');
    const opt = {
        margin: 1,
        filename: 'job-details.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    html2pdf().set(opt).from(element).save();
});