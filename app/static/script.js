async function fetchInsights() {
    const pageId = document.getElementById('pageIdInput').value.trim();
    if (!pageId) return;

    // UI Reset
    const btn = document.getElementById('searchBtn');
    const loader = document.getElementById('loader');
    const result = document.getElementById('result');
    
    btn.disabled = true;
    loader.style.display = 'block';
    result.style.display = 'none';

    try {
        // 1. Fetch Page Details
        const response = await fetch(`/api/v1/page/${pageId}`);
        if (!response.ok) throw new Error('Page not found');
        const data = await response.json();

        // 2. Update UI
        document.getElementById('profilePic').src = data.profile_pic_url || 'https://via.placeholder.com/100';
        document.getElementById('pageName').innerText = data.name;
        document.getElementById('pageUrl').href = data.url;
        document.getElementById('followerCount').innerText = data.followers_count.toLocaleString();
        document.getElementById('industry').innerText = data.industry || 'N/A';
        document.getElementById('headCount').innerText = data.head_count || 'N/A';
        document.getElementById('location').innerText = data.location || 'N/A';

        // Employees
        const empGrid = document.getElementById('employeesGrid');
        empGrid.innerHTML = '';
        if (data.employees && data.employees.length > 0) {
            data.employees.forEach(emp => {
                const div = document.createElement('div');
                div.className = 'stat-box';
                div.innerHTML = `
                    <div style="font-weight: bold;">${emp.name}</div>
                    <div style="font-size: 0.8rem; color: var(--text-secondary);">${emp.designation || 'Employee'}</div>
                `;
                empGrid.appendChild(div);
            });
        } else {
            empGrid.innerHTML = '<p style="color: var(--text-secondary);">No employee data publicly available.</p>';
        }

        result.style.display = 'block';

        // 3. Fetch AI Summary (Async)
        document.getElementById('aiSummaryText').innerText = "Generating analysis...";
        fetchSummary(pageId);

    } catch (error) {
        alert("Error fetching data: " + error.message);
    } finally {
        loader.style.display = 'none';
        btn.disabled = false;
    }
}

async function fetchSummary(pageId) {
    try {
        const response = await fetch(`/api/v1/page/${pageId}/summary`);
        const data = await response.json();
        document.getElementById('aiSummaryText').innerText = data.summary;
    } catch (e) {
        document.getElementById('aiSummaryText').innerText = "Could not generate summary.";
    }
}
