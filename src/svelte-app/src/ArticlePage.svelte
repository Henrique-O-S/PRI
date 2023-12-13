<!-- src/ResultsPage.svelte -->
<script>
  import { push, pop } from "svelte-spa-router";
  import Company from "./Company.svelte";
  export let params = {};
  console.log(params);
  let selectedArticle;
  let article;
  let companies;
  let company;
  let company_index = 0;
  $: {
    selectedArticle = params.id;
    article = {
      title: "Stocks are going absolutely mad",
      date: "2021-05-01",
      text: "Check out the companies making headlines in midday trading Monday. Colgate-Palmolive - Shares gained 2. 8% after Morgan Stanley upgraded the stock to overweight from equal weight and named it the top pick in the household and personal care industry. The firm said the stock was at a good price point after a recent selloff. Tesla - Shares dropped 2. 8% after Berenberg lowered its earnings estimate for Tesla by around 25% for 2023 following the company's price cuts for its electric vehicles. However, the firm upgraded the stock to buy from hold. GE HealthCare Technologies - The stock rose 4% after the company reported its first earnings after being spun off as a public company from General Electric. GE Healthcare's revenue came in at $4. 9 billion, an 8% year-over-year increase, and its fourth-quarter adjusted EPS was $1. 31. Ford Motor Company - Shares fell nearly 1. 4% after the company announced price cuts for its electric Mustang Mach-E crossover. The move in Ford comes after Tesla said earlier this month it would trim prices to counteract dwindling demand. Macy's - Goldman Sachs said Macy's is the best-positioned retailer and initiated coverage with a buy rating. The stock advanced 1. 8%. AMC Entertainment - Common shares of the theater chain fell by more than 7% after AMC announced a shareholder meeting in March for a potential change to its capital structure. The special meeting would allow shareholders to vote on increasing the total number of shares the company can issue and on a reverse stock split to convert its preferred shares to common shares. The preferred or \"APE\" shares, which trade at a large discount to the common shares, jumped by more than 16%. Carvana - Shares surged 28. 5% as an apparent short squeeze boosted the beleaguered stock. It was also briefly paused in early morning trading due to the rapid runup. Moderna - The vaccine producer fell another 3. 2%. The company's stock price has fallen about 7% since last week, after a Reuters report said the European Union is in talks with Pfizer and BioNTech to reduce the number of Covid-19 vaccine doses it's committed to purchasing this year in exchange for paying a higher price per dose. Advanced Micro Devices - Shares of semiconductor AMD fell 2. 1% after a slew of Wall Street analysts said they are worried about the company's upcoming earnings report following Intel's disastrous release. The company is scheduled to report Tuesday. - CNBC's Hakyung Kim, Jesse Pound, Alex Harring, Carmen Reinicke, Michelle Fox Theobald, and Samantha Subin contributed reporting.",
      url: "https://www.facebook.com/tools/ads-manager",
    };
    // split article text according to ". CAPITAL_LETTER"
    article.sentences = article.text
      .split(/\. (?=[A-Z])/)
    console.log(article.sentences);

    article.paragraphs = [article.sentences[0] + ". "];
    let currParagraph = 0;
    for (let i = 1; i < article.sentences.length; i++) {
      if (article.sentences[i].indexOf(" - ") !== -1) {
        currParagraph++;
        article.paragraphs.push(article.sentences[i] + ". ");
      } else {
        article.paragraphs[currParagraph] += (article.sentences[i] + ". ");
      }
    }
    console.log(article.paragraphs);

    companies = [
      {
        name: "Facebook",
        tag: "FB",
        description:
          "Facebook, Inc. is an American technology conglomerate based in Menlo Park, California.",
      },
      {
        name: "Apple",
        tag: "AAPL",
        description:
          "Apple Inc. is an American multinational technology company headquartered in Cupertino, California.",
      },
      {
        name: "Amazon",
        tag: "AMZN",
        description:
          "Amazon.com, Inc. is an American multinational technology company based in Seattle, Washington.",
      },
      {
        name: "Netflix",
        tag: "NFLX",
        description:
          "Netflix, Inc. is an American over-the-top content platform and production company headquartered in Los Gatos, California.",
      },
      {
        name: "Google",
        tag: "GOOGL",
        description:
          "Google LLC is an American multinational technology company that specializes in Internet-related services and products.",
      },
      {
        name: "Microsoft",
        tag: "MSFT",
        description:
          "Microsoft Corporation is an American multinational technology company with headquarters in Redmond, Washington.",
      },
      {
        name: "Tesla",
        tag: "TSLA",
        description:
          "Tesla, Inc. is an American electric vehicle and clean energy company based in Palo Alto, California.",
      },
      {
        name: "Twitter",
        tag: "TWTR",
        description:
          "Twitter is an American microblogging and social networking service on which users post and interact with messages known as tweets.",
      },
      {
        name: "Alphabet",
        tag: "GOOGL",
        description:
          "Alphabet Inc. is an American multinational conglomerate headquartered in Mountain View, California.",
      },
      {
        name: "Intel",
        tag: "INTC",
        description:
          "Intel Corporation is an American multinational corporation and technology company headquartered in Santa Clara, California.",
      },
      {
        name: "Nvidia",
        tag: "NVDA",
        description:
          "Nvidia Corporation is an American multinational technology company incorporated in Delaware and based in Santa Clara, California.",
      },
      {
        name: "PayPal",
        tag: "PYPL",
        description:
          "PayPal Holdings, Inc. is an American company operating an online payments system in majority of countries that supports online money transfers.",
      },
      {
        name: "Adobe",
        tag: "ADBE",
        description:
          "Adobe Inc. is an American multinational computer software company headquartered in San Jose, California.",
      },
    ];
    company = companies[company_index];
  }
  function updateCompany(inc) {
    company_index += inc;
    if (company_index < 0) {
      company_index = companies.length - 1;
    } else if (company_index >= companies.length) {
      company_index = 0;
    }
  }
</script>

<div class="content">
  <section class="articlePageTop">
    <div class="col">
      <div class="row">
        <h2 class="backButton" on:click={() => pop()}>&#8592;</h2>
      </div>
      <h1 class="articleTitle">{article.title}</h1>
      <div class="row articleDetails">
        <h5 class="date">{article.date}</h5>
        <a class="learnMore" href={article.url}>Learn more</a>
      </div>
    </div>
  </section>
  <hr />
  <div class="row" style="gap:10rem; padding-right:3rem;">
    <section class="text">
      {#each article.paragraphs as paragraph}
        <p>{paragraph}</p>
      {/each}
      <div style="margin-bottom: 2rem;"></div>
    </section>
    <section class="companyInfo">
      <Company {company} {updateCompany} />
    </section>
  </div>
</div>

<style>
  .content {
    width: 100%;
    margin: 2rem;
  }
  div.col {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 1rem;
  }
  div.row {
    display: flex;
    flex-direction: row;
  }
  section.articlePageTop {
    margin-bottom: 0.5rem;
  }

  h1.articleTitle {
    font-weight: 700;
    font-size: 2rem;
    color: #333;
    margin-top: 0rem;
  }

  h2.backButton {
    font-weight: 700;
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 0;
    padding-left: 0.5rem;
    text-align: start;
    cursor: pointer;
  }

  section.text {
    text-align: justify;
    font-size: 1.1rem;
    text-indent: 1rem;
    padding-left: 1rem;
    margin-bottom: 0.2rem;
    font-weight: 500;
    margin-top: 2rem;
    width: 60%;
  }

  section.text p {
    line-height: 1.7rem;
  }

  section.companyInfo {
    flex: 1;
  }

  hr {
    margin-bottom: 1rem;
    margin-top: 0rem;
    background-color: silver;
    height: 1.5px;
    opacity: 30%;
  }

  .articleDetails {
    justify-content: space-between;
    margin-left: 1rem;
    margin-right: 1rem;
    align-items: center;
  }

  .articleDetails * {
    margin-bottom: 0;
  }

  .articleDetails .date {
    font-size: 0.9rem;
    opacity: 0.5;
  }

  .articleDetails .learnMore {
    font-size: 1rem;
    cursor: pointer;
    color: rgb(81, 81, 225);
  }
</style>
