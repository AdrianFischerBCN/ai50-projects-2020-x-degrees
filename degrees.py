import csv
import sys


from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}

            else:
                names[row["name"].lower()].add(row["id"])


    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass



def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

def Iteracion():
    """
    Que hace iteration?
    Iteration se ejecuta solamente cuando hay algo en la Frontera
        1) Elimina el primer vecino de la frontera
        2) Busca los vecinos
    """

    NeighborList = neighbors_for_person(Actor)

    PathDeclaration["Explored"].append(Frontier[0])
    del Frontier[0]

    for Neighbor in NeighborList:
        NombreVecino = Neighbor[1]
        PeliculaVecino = Neighbor[0]

        if ((NombreVecino not in Frontier) and (NombreVecino not in PathDeclaration["Explored"])):
            PathDeclaration["Previous"].append(Actor)
            PathDeclaration["MovieLink"].append(PeliculaVecino)
            Frontier.append(NombreVecino)

    print("Currently in Frontier: ",Frontier)
    print("Already explored: ", PathDeclaration["Explored"])
    print("Coming from: ", PathDeclaration["Previous"])
    print("Movielink is: ", PathDeclaration["MovieLink"])



def shortest_path(source, target):

    global PathDeclaration
    global Actor
    global Frontier

    PathDeclaration = {
        "Explored": [],
        "Previous": ["Start. So no previous"],
        "MovieLink": ["Start. So no movielink"]
    }

    Target = target
    Actor = source
    Found = False
    Frontier = [Actor]
    NeighborList = neighbors_for_person(Actor)
    print(NeighborList)
    print("")
    print("Initial Situation")
    print(Actor)
    print("")
    Iteracion()

    while not len(Frontier) == 0:
        Actor=Frontier[0]
        print("""
        """)
        print("Next Iteration. Actor is: "+Actor)
        NeighborList=neighbors_for_person(Actor)

        print(Frontier)
        print(len(Frontier))
        Iteracion()
        if len(Frontier)==0:
            break

        if(Frontier[0]==Target):
            Found=True
            break

        a = len(Frontier)
    print(Found)

    if Found:
        """
        El siguiente que iba a salir del Frontier era el Explored
        Por eso, lo metemos en explored
        Luego vamos a iterar hacia atrás hasta encontrar uno a uno los nodos. 
        Habremos acabado cuando el previous sea "Start. So no previous" Es decir, cuando lleguemos al origen de la búsqueda
        Dentro del while
            El link estará formado por
                La película: lo encontramos en el MovieLink
                El destino: Lo encontramos en la correspondiente posición del Explored
                Recordatorio: Siempre en una misma posición tenemos el nexo (MovieLink), el origen (Previous) y el destino (Explored)
    
            Con el link, lo añadimos en el ChosenPath. 
            Además, lo añadimos en el ChosenPathCorrected, pero en este caso cada nuevo link va a ir al principio
            Realmente, el ChosenPath no me hubiese hecho falta y podría haberlo hecho todo con el ChosenPathCorrected
            Pero ya lo había implementado con el ChosenPath normal, que va de final a principio
        """
        PathDeclaration["Explored"].append(Frontier[0])
        AuxCounter = len(PathDeclaration["Explored"]) - 1
        ChosenPath = []
        ChosenPathCorrected = []
        while PathDeclaration["Previous"][AuxCounter] != "Start. So no previous":
            NewLink = ((PathDeclaration["MovieLink"][AuxCounter]), (PathDeclaration["Explored"][AuxCounter]))
            ChosenPath.append(NewLink)
            AuxCounter = PathDeclaration["Explored"].index((PathDeclaration["Previous"][AuxCounter]))
            ChosenPathCorrected.insert(0, NewLink)

        z=ChosenPathCorrected

    else:
        z= None


    return(z)



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]





if __name__ == "__main__":
    main()
© 2020 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
