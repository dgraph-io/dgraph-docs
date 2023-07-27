+++
date = "2017-03-20T19:35:35+11:00"
title = "Get started with Dgraph"
description = "From learning the basics of graph databases to advanced functions and capabilities, Dgraph docs have the information you need."
aliases = ["/contribute"]
[menu.main]
  name = "Home"
  identifier = "home"
  weight = 1
+++

<div class="container">
  <div class="landing">
    <div class="hero">
      <p class="title-tag">Docs</p>
      <h1>Get started with Dgraph</h1>
      <p>
        Designed from the ground up to be run in production, Dgraph is the native GraphQL database with a graph backend. It is open-source, scalable, distributed, highly available and lightning fast.
      </p>
      <p><b>Tip</b>: New to Dgraph? Take the <a href="https://dgraph.io/tour/">Dgraph Tour</a> to run live queries in your browser. Then, try Dgraph as a <a href="https://cloud.dgraph.io">cloud service</a>, or <a href='{{< relref "deploy/installation/_index.md">}}'>download</a> Dgraph to deploy it yourself.</p>
    </div>
    <div class="item">
      <a href="{{< relref "dgraph-overview.md">}}">
        <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
          <circle cx="10.5" cy="10.5" r="6.5" stroke="#EF265A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M17 17L20 20" stroke="#100C19" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <h2>Overview</h2>
        <p>
        Understand Dgraph core concepts and hosting options.
        </p>
      </a>
    </div>
    <div class="item">
      <a  href="{{< relref "graphql/_index.md">}}">
        <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M2.52691 17.6612L3.37109 18.1592L12.7756 1.51639L11.9315 1.01839L2.52691 17.6612Z" fill="#100C19"/>
          <path d="M21.1509 16.332H2.3418V17.328H21.1509V16.332Z" fill="#100C19"/>
          <path d="M2.71302 16.8914L12.1211 22.4414L12.6085 21.5789L3.20042 16.0289L2.71302 16.8914Z" fill="#100C19"/>
          <path d="M10.8888 2.42656L20.2969 7.97656L20.7843 7.11403L11.3762 1.56403L10.8888 2.42656Z" fill="#100C19"/>
          <path d="M2.71181 7.11012L3.19922 7.97266L12.6073 2.42266L12.1199 1.56012L2.71181 7.11012Z" fill="#100C19"/>
          <path d="M10.7107 1.51639L20.1152 18.1592L20.9594 17.6612L11.5549 1.01839L10.7107 1.51639Z" fill="#100C19"/>
          <path d="M4.0627 6.44922H3.08789V17.5492H4.0627V6.44922Z" fill="#100C19"/>
          <path d="M20.4104 6.4502H19.4355V17.5502H20.4104V6.4502Z" fill="#100C19"/>
          <path d="M11.5235 21.2661L11.9492 22.0195L20.1317 17.1925L19.706 16.4391L11.5235 21.2661Z" fill="#100C19"/>
          <path d="M21.6995 17.874C21.1357 18.876 19.879 19.218 18.8984 18.642C17.9177 18.066 17.583 16.782 18.1467 15.78C18.7104 14.778 19.9671 14.436 20.9478 15.012C21.9344 15.594 22.2691 16.872 21.6995 17.874Z" fill="#EF265A"/>
          <path d="M5.34009 8.21973C4.77635 9.22173 3.51967 9.56373 2.53899 8.98773C1.55831 8.41173 1.22358 7.12773 1.78733 6.12573C2.35107 5.12373 3.60775 4.78173 4.58843 5.35773C5.56911 5.93973 5.90384 7.21773 5.34009 8.21973Z" fill="#EF265A"/>
          <path d="M1.79319 17.874C1.22944 16.872 1.56416 15.594 2.54485 15.012C3.52553 14.436 4.77634 14.778 5.34595 15.78C5.9097 16.782 5.57497 18.06 4.59429 18.642C3.60774 19.218 2.35693 18.876 1.79319 17.874Z" fill="#EF265A"/>
          <path d="M18.1545 8.21973C17.5908 7.21773 17.9255 5.93973 18.9062 5.35773C19.8869 4.78173 21.1377 5.12373 21.7073 6.12573C22.271 7.12773 21.9363 8.40573 20.9556 8.98773C19.9749 9.56373 18.7183 9.22173 18.1545 8.21973Z" fill="#EF265A"/>
          <path d="M11.7487 23.7476C10.6153 23.7476 9.69922 22.8116 9.69922 21.6536C9.69922 20.4956 10.6153 19.5596 11.7487 19.5596C12.882 19.5596 13.7981 20.4956 13.7981 21.6536C13.7981 22.8056 12.882 23.7476 11.7487 23.7476Z" fill="#EF265A"/>
          <path d="M11.7487 4.43995C10.6153 4.43995 9.69922 3.50395 9.69922 2.34595C9.69922 1.18795 10.6153 0.251953 11.7487 0.251953C12.882 0.251953 13.7981 1.18795 13.7981 2.34595C13.7981 3.50395 12.882 4.43995 11.7487 4.43995Z" fill="#EF265A"/></svg>
        <h2>GraphQL API</h2>
        <p>
          Generate a GraphQL API and a graph backend from a simple GraphQL schema.
        </p>
      </a>
    </div>
    <div class="item">
      <a href="{{< relref "dql/_index.md">}}">
      <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M21.9995 14.6L21.9995 20.4C21.9995 20.7314 21.7309 21 21.3995 21L17.5995 21C17.2681 21 16.9995 20.7314 16.9995 20.4L16.9995 14.6C16.9995 14.2686 17.2681 14 17.5995 14L21.3995 14C21.7309 14 21.9995 14.2686 21.9995 14.6Z" stroke="#100C19" stroke-width="1.33333"/>
        <path d="M6.99951 9.1L6.99951 14.9C6.99951 15.2314 6.73088 15.5 6.39951 15.5L2.59951 15.5C2.26814 15.5 1.99951 15.2314 1.99951 14.9L1.99951 9.1C1.99951 8.76863 2.26814 8.5 2.59951 8.5L6.39951 8.5C6.73088 8.5 6.99951 8.76863 6.99951 9.1Z" stroke="#EF265A" stroke-width="1.33333"/>
        <path d="M21.9995 3.6L21.9995 9.4C21.9995 9.73137 21.7309 10 21.3995 10L17.5995 10C17.2681 10 16.9995 9.73137 16.9995 9.4L16.9995 3.6C16.9995 3.26863 17.2681 3 17.5995 3L21.3995 3C21.7309 3 21.9995 3.26863 21.9995 3.6Z" stroke="#100C19" stroke-width="1.33333"/>
        <path d="M16.9995 17.5L13.4995 17.5C12.3949 17.5 11.4995 16.6046 11.4995 15.5L11.4995 8.5C11.4995 7.3954 12.3949 6.5 13.4995 6.5L16.9995 6.5" stroke="#100C19" stroke-width="1.33333"/>
        <path d="M11.4995 12L6.99951 12" stroke="#100C19" stroke-width="1.33333"/></svg>
        <h2>Dgraph Query Language (DQL)</h2>
        <p>
          Learn Dgraph Query Language (DQL), Dgraph’s proprietary language to add, modify, delete and fetch data.
        </p>
      </a>
    </div>
    <div class="item">
      <a href="{{< relref "/dgraphcloud">}}">
        <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M12 22V13M12 13L15.5 16.5M12 13L8.5 16.5" stroke="#100C19" stroke-width="1.71429" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M20 17.6073C21.4937 17.0221 23 15.6889 23 13C23 9 19.6667 8 18 8C18 6 18 2 12 2C6 2 6 6 6 8C4.33333 8 1 9 1 13C1 15.6889 2.50628 17.0221 4 17.6073" stroke="#EF265A" stroke-width="1.71429" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <h2>Dgraph Cloud</h2>
        <p>
          Run Dgraph in the Cloud.
          Work with your data in a fully-managed cloud service.
        </p>
      </a>
    </div>
    <div class="item">
      <a href="{{< relref "deploy/_index.md">}}">
        <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="#EF265A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M19.6224 10.3954L18.5247 7.7448L20 6L18 4L16.2647 5.48295L13.5578 4.36974L12.9353 2H10.981L10.3491 4.40113L7.70441 5.51596L6 4L4 6L5.45337 7.78885L4.3725 10.4463L2 11V13L4.40111 13.6555L5.51575 16.2997L4 18L6 20L7.79116 18.5403L10.397 19.6123L11 22H13L13.6045 19.6132L16.2551 18.5155C16.6969 18.8313 18 20 18 20L20 18L18.5159 16.2494L19.6139 13.598L21.9999 12.9772L22 11L19.6224 10.3954Z" stroke="black" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <h2>Self-hosted cluster</h2>
        <p>
          Install and manage a Dgraph cluster in a variety of self-managed deployment scenarios.
        </p>
      </a>
    </div>
    <div class="item">
      <a href="{{< relref "clients">}}">
      <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M14 4L10 20" stroke="#EF265A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M5 8L1 12L5 16" stroke="black" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M19 8L23 12L19 16" stroke="black" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <h2>gRPC and HTTP Clients</h2>
        <p>
          Interact with a Dgraph cluster using libraries in various programming languages.
        </p>
      </a>
    </div>

  </div>

  <!-- Join the Community -->

  <div class="join-the-community">
    <div class="community-heading">
      <h3>Join the Community</h3>
      <p>Our mission is to help developers and organizations leverage the power of graph and GraphQL to build applications better, faster, and more easily.</p>
    </div>
    <div class="community-buttons">
      <div class="community-item big-card black-card">
        <svg class="community-icon" xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80" fill="none">
        <path d="M17.2188 58.2883L32.2432 71.0002H49.8583L52.4487 66.9324L66.9551 46.0849L59.1838 21.1697L50.8944 17.6104L30.6891 18.6273L22.3998 21.1697C19.6366 27.1019 14.0066 39.068 13.5922 39.4748C13.1777 39.8815 15.8372 52.1866 17.2188 58.2883Z" fill="#161614"/>
        <path d="M41.0002 11C24.4337 11 11 24.7413 11 41.6928C11 55.2537 19.596 66.7587 31.516 70.8172C33.0153 71.1013 33.5658 70.1514 33.5658 69.3407C33.5658 68.6088 33.5379 66.191 33.525 63.6263C25.1789 65.483 23.4178 60.005 23.4178 60.005C22.0531 56.4573 20.0868 55.514 20.0868 55.514C17.3649 53.609 20.292 53.6482 20.292 53.6482C23.3045 53.8647 24.8908 56.8111 24.8908 56.8111C27.5665 61.5033 31.909 60.1468 33.6209 59.3625C33.8902 57.3788 34.6676 56.0248 35.5256 55.2583C28.8621 54.4822 21.8574 51.8504 21.8574 40.0898C21.8574 36.7388 23.0293 34.0008 24.9484 31.8514C24.6369 31.0783 23.6101 27.9566 25.239 23.7289C25.239 23.7289 27.7583 22.904 33.4912 26.875C35.8843 26.195 38.4507 25.8539 41.0002 25.8422C43.5498 25.8539 46.1182 26.195 48.5157 26.875C54.2417 22.904 56.7575 23.7289 56.7575 23.7289C58.3904 27.9566 57.3631 31.0783 57.0516 31.8514C58.9752 34.0008 60.1391 36.7388 60.1391 40.0898C60.1391 51.8784 53.121 54.4741 46.4406 55.2339C47.5167 56.1864 48.4755 58.0543 48.4755 60.9178C48.4755 65.0246 48.4407 68.3298 48.4407 69.3407C48.4407 70.1575 48.9807 71.1145 50.5014 70.8131C62.4149 66.7501 71 55.2492 71 41.6928C71 24.7413 57.5682 11 41.0002 11ZM22.2361 54.7226C22.17 54.8751 21.9355 54.9208 21.7219 54.8161C21.5043 54.716 21.3821 54.5081 21.4526 54.3551C21.5172 54.1981 21.7522 54.1544 21.9693 54.2596C22.1874 54.3597 22.3116 54.5696 22.2361 54.7226ZM23.7117 56.0697C23.5687 56.2054 23.289 56.1424 23.0992 55.9279C22.903 55.714 22.8662 55.4278 23.0113 55.2901C23.1588 55.1544 23.4301 55.2179 23.6268 55.4319C23.823 55.6484 23.8613 55.9325 23.7117 56.0697ZM24.7241 57.7933C24.5403 57.924 24.2397 57.8015 24.0539 57.5285C23.8701 57.2556 23.8701 56.9283 24.0579 56.7972C24.2442 56.666 24.5403 56.7839 24.7286 57.0548C24.9119 57.3323 24.9119 57.6597 24.7241 57.7933ZM26.4363 59.7895C26.2718 59.975 25.9216 59.9252 25.6652 59.6721C25.4029 59.4246 25.3299 59.0734 25.4948 58.8879C25.6613 58.7018 26.0135 58.7542 26.2718 59.0053C26.5321 59.2523 26.6116 59.606 26.4363 59.7895ZM28.649 60.4634C28.5765 60.7038 28.2392 60.8131 27.8994 60.7109C27.5601 60.6057 27.338 60.3241 27.4066 60.0812C27.4771 59.8393 27.8159 59.7254 28.1582 59.8347C28.497 59.9394 28.7196 60.2189 28.649 60.4634ZM31.1673 60.7493C31.1757 61.0024 30.8876 61.2123 30.5309 61.2169C30.1722 61.225 29.8821 61.0202 29.8781 60.7711C29.8781 60.5154 30.1598 60.3076 30.5184 60.3015C30.8751 60.2944 31.1673 60.4977 31.1673 60.7493ZM33.6411 60.6522C33.6839 60.8992 33.436 61.1529 33.0817 61.2205C32.7335 61.2855 32.4111 61.133 32.3669 60.8881C32.3236 60.6349 32.576 60.3813 32.9238 60.3158C33.2785 60.2527 33.5959 60.4011 33.6411 60.6522Z" fill="#F4F4F4"/></svg>
        <div class="community-info">
          <h6>Contribute to Dgraph</h6>
          <p>View tracker and issues</p>
        </div>
        <a href="https://github.com/dgraph-io/dgraph" class="button" target="_blank">Github</a>
      </div>
      <div class="community-item big-card red-card">
        <svg class="community-icon" xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80" fill="none">
          <path d="M66.2339 29.3771L66.2349 29.3793C72.2704 43.947 65.3462 60.6383 50.7832 66.6729L50.7821 66.6733C46.2557 68.5523 41.5348 69.1734 36.9917 68.707L35.2859 68.5319L34.8752 70.1967C34.3646 72.2662 32.9214 74.0644 30.8056 74.9419L30.8035 74.9427C27.2737 76.4115 23.223 74.7312 21.7613 71.1982L21.7605 71.1963C20.8849 69.0861 21.1375 66.7976 22.2448 64.965L23.1311 63.4982L21.8026 62.4157C18.2576 59.5273 15.3583 55.7519 13.4906 51.2285L13.4896 51.2263C7.45407 36.6586 14.3783 19.9673 28.9413 13.9327L28.9424 13.9323C33.4688 12.0533 38.1897 11.4322 42.7329 11.8986L44.4386 12.0737L44.8493 10.4089C45.3599 8.33941 46.8031 6.54121 48.9189 5.66374L48.921 5.66284C52.4508 4.19408 56.5015 5.87444 57.9632 9.4074L57.964 9.40932C58.8396 11.5195 58.587 13.808 57.4797 15.6406L56.5934 17.1074L57.9219 18.1899C61.4669 21.0783 64.3662 24.8537 66.2339 29.3771Z" fill="#100C19" stroke="#100C19" stroke-width="3.94497"/>
          <path d="M43.8246 30.7382L43.7414 30.9402H54.7223L42.244 43.4146H53.3437L31.5365 65.2153C31.9643 65.6311 32.309 66.13 32.5466 66.7122C33.5449 69.1358 32.3922 71.9158 29.9797 72.9138C28.7675 73.4246 27.4603 73.3771 26.3432 72.9138C25.7846 72.6881 25.2617 72.3554 24.8339 71.9158C24.3942 71.4881 24.0258 70.9535 23.7762 70.3476C22.7661 67.924 23.9189 65.1558 26.3432 64.146C27.5554 63.647 28.8626 63.6827 29.9797 64.146L35.9692 49.6756V49.64H24.9052L37.3834 37.1655H26.2838L48.1385 15.3174C47.7345 14.9135 47.4136 14.4145 47.1759 13.8561C46.1777 11.4325 47.3185 8.66436 49.7428 7.65452C50.955 7.15554 52.2623 7.19119 53.3794 7.6664C53.9142 7.88025 54.4133 8.20102 54.8411 8.61684C55.3046 9.05641 55.6849 9.59103 55.9463 10.2207C56.9446 12.6443 55.8037 15.4243 53.3794 16.4223C52.1672 16.9213 50.8718 16.8856 49.7547 16.4223L43.8246 30.7263V30.7382Z" fill="white"/></svg>
        <div class="community-info">
          <h6>Contribute to Dgraph</h6>
          <p>View tracker and issues</p>
        </div>
        <a href="https://discuss.dgraph.io/" class="button" target="_blank">Discuss</a>
      </div>
    </div>

  </div>
</div>

<style>
  .content-wrapper {
    margin: 0 auto;
    max-width: 100%;
    border: none;
  }
  article {
    max-width: none;
  }
  article h1 {
    border: none;
  }
  #sidebar {
    display: none;
  }
  article h1.post-title {
    display: none;
  }

  @media all and (min-width:800px) {
    .content-wrapper {
      padding-top: 76px;
    }
  }
</style>
