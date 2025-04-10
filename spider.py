import scrapy
OUR_TEAM_NAMES = set(["bloop dreams", "small baller brand", "father figures"])

class SoftballSpider(scrapy.Spider):
    name = 'Cerritos MLS'
    start_urls = ['https://www.mlsoftball.com/programs/stats/1/spring-2025/1398/cerritos']

    def parse(self, response):
        for opt in response.css("#conditions-season > option::attr(data-url)"):
            yield scrapy.Request(response.urljoin(opt.get()), callback=self.parse_season)
            
    def parse_season(self, response):
        for title in response.css("body > div.text-content > div.container > div > div.condition > div.schedule-row"):
            tester = title.css("div:nth-child(1)::text").get()
            
            if tester is not None and (tester.strip().startswith("TUE") or tester.strip().startswith("WED")):
                for links in title.css("div.right > a"):
                    if links.css("::text").get().strip() == "League Standings":
                        yield response.follow(links, self.parse_standings)

    def parse_standings(self, response):
        for team in response.css("#scores_table > tbody > tr"):
            teamname = team.css("td > a::text").get()
            if teamname is not None and teamname.lower() in OUR_TEAM_NAMES:
                follow = team.css("td > a::attr(href)").get()
                yield scrapy.Request(response.urljoin(follow), callback=self.parse_team)

    def parse_team(self, response):
        season = response.css("body > div.text-content > div > div > span.StoryHeadline::text").get()
        header = response.css("#scores_table > thead")
        columns = []
        for h in header.css("th::text"):
            columns.append(h.get())

        players = []
        for playerrow in response.css("#scores_table > tbody > tr"):
            player = [stat.get() for stat in playerrow.css("td::text")]
            players.append(player)
        yield {
            "season" : season,
            "players": players
        }
