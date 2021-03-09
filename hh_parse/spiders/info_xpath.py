_page_selectors = {
    "pages": "//div[@data-qa='pager-block']//a[@data-qa='pager-page']/@href",
    "vacancies": "//div[@class='vacancy-serp']//a[@data-qa='vacancy-serp__vacancy-title']/@href",
    "employer_page": "//div[@class='vacancy-serp']//a[@class='bloko-link bloko-link_secondary']/@href",
    "employer_vacancies_page": "//div[@id='HH-React-Root']//"
                               "a[@data-qa='employer-page__employer-vacancies-link']/@href",

}

_vacancy_info = {
    "title": '//h1[@data-qa="vacancy-title"]/text()',
    "salary": '//p[@class="vacancy-salary"]/span/text()',
    "description": '//div[@data-qa="vacancy-description"]//text()',
    "key_skills": '//div[@class="bloko-tag-list"]//div[contains(@data-qa, "skills-element")]/'
                  'span[@data-qa="bloko-tag__text"]/text()',
    "employer_url": '//a[@data-qa="vacancy-company-name"]/@href',
}

_employer_info = {
    "employer": "//div[@id='HH-React-Root']//span[@data-qa='company-header-title-name']/text()",
    "employer_website": "//div[@id='HH-React-Root']//a[@data-qa='sidebar-company-site']/@href",
    "employer_description": "//div[@id='HH-React-Root']//div[@class='g-user-content']/p/text()",
    "business_segments": "//div[contains(text(), 'Сферы деятельности')]/following-sibling::p/text()"
}
