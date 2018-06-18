from imdb import IMDb
from .film import Film


class movieSearch:
    __obj = IMDb()

    @classmethod
    def search_1(cls, title):
        movies = cls.__obj.search_movie(title, 2)
        result = []
        movie = cls.__obj.get_movie(movies[0].movieID)
        temp = cls.__fill(movie)
        if temp is None:
            return None
        result.append(temp)
        persons = []
        count = min(3, len(temp.actors))
        for i in range(count):
            persons.append(temp.actors[i]['id'])
        persons.append(temp.director[0]['id'])
        movieIds = set()
        for personId in persons:
            person = cls.__obj.get_person_filmography(personId)
            filmGraphs = person["data"]["filmography"][0]
            if filmGraphs.__contains__('actor'):
                # 演员,扮演过的作品
                filmGraphs = filmGraphs['actor']
            elif filmGraphs.__contains__('writer'):
                # 编剧,编辑过的作品
                filmGraphs = filmGraphs['writer']
            else:
                # 导演,导演过的作品
                filmGraphs = filmGraphs['director']
            count = 0
            for film in filmGraphs:
                if count > 5:
                    break
                name = film['title']
                if 'None' in name:
                    continue
                movieIds.add(film.movieID)
                count += 1
        temp = []
        count = 0
        # 按评价排序,取前5个
        for movieId in movieIds:
            if movieId == movies[0].movieID:
                continue
            movie = cls.__obj.get_movie(movieId)
            film = cls.__fill(movie)
            if film is None:
                continue
            if count == 5:
                rating = float(film.rating)
                for i in range(5):
                    if rating > float(temp[i].rating):
                        temp[i] = film
            else:
                temp.append(film)
            count += 1
        result.extend(temp)
        return result

    @classmethod
    def search_2(cls, start):
        # 推荐top5
        movies = cls.__obj.get_top250_movies()
        result = []
        count = len(movies)
        if count - start < 5:
            start = max(count - 5, 0)
        c = 0
        for i in range(count):
            if i < start:
                continue
            if i - start - c > 4:
                break
            movieId = movies[i].movieID
            movie = cls.__obj.get_movie(movieId)
            film = cls.__fill(movie)
            if film is None:
                c += 1
            else:
                result.append(film)
        return result

    @staticmethod
    def __fill(film):
        try:
            movie = Film()
            movie.title = film["title"]
            movie.coverUrl = film["cover url"]
            movie.genres = film["genres"]
            movie.actors = movieSearch.parsePerson(film["cast"])
            movie.countries = film["countries"]
            movie.director = movieSearch.parsePerson(film["directors"])
            movie.languages = film["languages"]
            movie.originalAirDate = film["original air date"]
            movie.plotOutline = film["plot outline"]
            movie.rating = film["rating"]
            movie.runTimes = film["runtimes"]
            return movie
        except KeyError:
            return None

    @staticmethod
    def parsePerson(persons):
        result = []
        count = min(5, len(persons))
        for i in range(count):
            temp = {'id': persons[i].personID, 'name': persons[i]['name']}
            result.append(temp)
        return result