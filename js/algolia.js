
const algolia = document.getElementById('algolia-search');
const searchClient = algoliasearch( algolia.dataset.a, algolia.dataset.k);

const search = instantsearch({
    indexName: algolia.dataset.i,
    searchClient,
    routing: true,
});

search.addWidgets([
    instantsearch.widgets.configure({
        hitsPerPage: 10,
    })
]);

search.addWidgets([
    instantsearch.widgets.searchBox({
        container: '#search-box',
        placeholder: '搜索文章',
    })
]);

search.addWidget(
    instantsearch.widgets.pagination({
      container: '#pagination',
    })
  );

search.addWidgets([
    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            item(hit){
                // document.getElementById('hit-template').innerHTML,
                let title = hit.title ? hit.title : '';
                let suffix = hit.title.length > 10 ? '...' : '';
                title = title.replace(/—+/ig, '-');
                title = title.substring(0, Math.min(10, hit.title.length))+suffix;
                return `
                    <div class="hits-block">
                        <a href="${hit.url}" title="${hit.title}">${title}</a>
                    </div>
                `
            },
            empty: `没有找到 <em>"{{query}}"</em> 相关的内容`,
        },
    })
]);

search.start();