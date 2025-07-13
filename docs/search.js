let data = {orthologs: [], strains: []};

async function loadData() {
  try {
    const res = await fetch('data.json'); // If this fails, try './data.json' or '../docs/data.json'
    data = await res.json();
    console.log('Loaded data:', data); // Debug: log loaded data
  } catch (e) {
    console.error('Failed to load data', e);
  }
}

function createLink(url, text) {
  const a = document.createElement('a');
  a.href = url;
  a.textContent = text;
  a.target = '_blank';
  return a;
}

function renderResults(orthologs, strains) {
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = '';

  if (orthologs.length) {
    const h = document.createElement('h3');
    h.textContent = 'Ortholog Table';
    resultsDiv.appendChild(h);
    const table = document.createElement('table');
    table.innerHTML = `<tr><th>C. elegans Gene</th><th>Human Gene</th></tr>`;
    orthologs.forEach(o => {
      const tr = document.createElement('tr');
      const ceLink = createLink(`https://wormbase.org/search/gene/${o.ce_gene}`, o.ce_gene);
      // WormBase handles both worm and human genes under the same search
      // endpoint.  Using `search/gene` avoids "No such gene" errors when
      // linking to human gene symbols.
      const humanLink = createLink(`https://wormbase.org/search/gene/${o.human_gene}`, o.human_gene);
     const td1 = document.createElement('td');
      td1.appendChild(ceLink);
      tr.appendChild(td1);
      const td2 = document.createElement('td');
      td2.appendChild(humanLink);
      tr.appendChild(td2);
      table.appendChild(tr);
    });
    resultsDiv.appendChild(table);
  }

  if (strains.length) {
    const h = document.createElement('h3');
    h.textContent = 'Temperature Sensitive Strains';
    resultsDiv.appendChild(h);
    const table = document.createElement('table');
    table.innerHTML = `<tr><th>Strain</th><th>C. elegans Gene</th><th>Human Gene</th><th>Phenotype</th></tr>`;
    strains.forEach(s => {
      const tr = document.createElement('tr');
      const strainLink = createLink(`https://wormbase.org/search/strain/${s.strain_name}`, s.strain_name);
      const ceGeneLink = createLink(`https://wormbase.org/search/gene/${s.ce_gene}`, s.ce_gene);
      const humanText = s.human_gene || s.human_stable_id;
      // Use the generic gene search endpoint for human genes as well
      const humanLink = createLink(`https://wormbase.org/search/gene/${humanText}`, humanText);
      const tdStrain = document.createElement('td');
        tdStrain.appendChild(strainLink);
        tr.appendChild(tdStrain);
      const td2 = document.createElement('td');
      td2.appendChild(ceGeneLink);
      tr.appendChild(td2);
      const td3 = document.createElement('td');
      td3.appendChild(humanLink);
      tr.appendChild(td3);
      tr.appendChild(Object.assign(document.createElement('td'), {textContent: s.phenotype}));
      table.appendChild(tr);
    });
    resultsDiv.appendChild(table);
  }

  if (!orthologs.length && !strains.length) {
    resultsDiv.textContent = 'No matches found.';
  }
}

function search(query) {
  const q = query.trim().toLowerCase();
  if (!q) {
    document.getElementById('results').innerHTML = '';
    return;
  }
  const orth = data.orthologs.filter(o =>
    o.ce_gene.toLowerCase().includes(q) ||
    o.human_gene.toLowerCase().includes(q));
  const str = data.strains.filter(s =>
    s.strain_name.toLowerCase().includes(q) ||
    s.ce_gene.toLowerCase().includes(q) ||
    (s.human_gene && s.human_gene.toLowerCase().includes(q)));
  renderResults(orth, str);
}

document.addEventListener('DOMContentLoaded', () => {
  loadData();
  const input = document.getElementById('searchInput');
  input.addEventListener('input', () => search(input.value));
});