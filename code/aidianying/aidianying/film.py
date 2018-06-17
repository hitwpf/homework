class Film:
    title = ''
    actors = ''
    genres = ''
    runTimes = ''
    originalAirDate = ''
    rating = ''
    coverUrl = ''
    plotOutline = ''
    languages = ''
    countries = ''
    director = ''

    def toJson(self):
        result = {
            "title": self.title,
            "actors": [x['name'] for x in self.actors],
            "genres": self.genres,
            "runTimes": self.runTimes,
            "originalAirDate": self.originalAirDate,
            "rating": self.rating,
            "coverUrl": self.coverUrl,
            "plotOutline": self.plotOutline,
            "languages": self.languages,
            "countries": self.countries,
            "director": [x['name'] for x in self.director]
        }
        return result
