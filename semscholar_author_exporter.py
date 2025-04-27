from collections import defaultdict
from semanticscholar import SemanticScholar

sch = SemanticScholar()

AUTHOR='Anjith George'
results = sch.search_author(AUTHOR)
print(f'{results.total} results.')

papers=[]

for res in results:
    papers.extend(res['papers'])
    
print(f'{len(papers)} papers found for {AUTHOR}.')

for paper in papers:

    if isinstance(paper, dict):
        print("This item is a dictionary:")
    else:
        print("Error: ", type(paper))

# sort by year
papers = sorted(papers, key=lambda x: x.get('year', float('inf')), reverse=True)

html_content = '''<html>
<head>
<style>
details, h2 { margin-bottom: 20px; }
.doi-link { color: green; }
.bold { font-weight: bold; }
.abstract-box {
    padding: 10px;
    margin-top: 5px;
    background-color: #f9f9f9;
    border-left: 5px solid #2196F3; /* Blue */
    font-style: italic;
}
</style>
</head>
<body>'''

# Group papers by year
papers_by_year = defaultdict(list)
for paper in papers:
    year = paper.get('year', 'Year not available')
    papers_by_year[year].append(paper)

# Sort the years to display them in order
sorted_years = sorted(papers_by_year.keys(), reverse=True)  # Sort descending, newest first

# Generate HTML content with headers for each year
for year in sorted_years:
    html_content += f'<h2>{year}</h2>'
    for paper in papers_by_year[year]:
        # Retrieve abstract or use default text if it's None or missing
        abstract = paper.get('abstract') or "No abstract available."
        # Create a string of authors, highlighting a specific name
        authors = ', '.join([f"<span class='bold'>Anjith George</span>" if 'Anjith George' in author['name'] else author['name'] for author in paper.get('authors', [])])
        # Fetch DOI or set default if missing
        doi = paper['externalIds'].get('DOI', 'Not available')
        doi_link = f'<a href="https://doi.org/{doi}" class="doi-link">doi:{doi}</a>' if doi != 'Not available' else 'DOI not available'

        # Generate HTML content for each paper
        html_content += f'''<details>
            <summary>{authors}.
    <span class="bold">{paper['title']}</span>.
    <em>{paper.get('venue', 'Not available')}</em>, {year}.
    {doi_link} | <a href="{paper.get('url', '#')}" target="_blank">URL</a></summary>
    <div class="abstract-box"><span class="bold">Abstract:</span> {abstract}</div>
          </details>'''

html_content += '</body></html>'

# Save to an HTML file
with open('papers_by_year.html', 'w') as f:
    f.write(html_content)

print("HTML content generated and sorted by year, saved to papers_by_year.html")
