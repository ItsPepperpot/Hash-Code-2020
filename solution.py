import sys
from collections import defaultdict, Counter


class Library(object):
    def __init__(self, id, num_of_books, sign_up_time, books_per_day):
        self.id = id
        self.num_of_books = num_of_books
        self.books = []
        self.sign_up_time = sign_up_time
        self.books_per_day = books_per_day
        self.score = 0

    def calculate_score(self):
        self.score = sum([book.score for book in self.books])

    def __repr__(self):
        return f"Library {self.id}"


class Book(object):
    def __init__(self, score, id):
        self.score = score
        self.id = id

    def __repr__(self):
        return f"Book {self.id}"


def solve_3(books, libraries, days):
    output = []
    books_already_done = []
    # Sort libraries by their score
    for library in sorted(libraries, reverse=True, key=lambda l: l.score):
        books_by_score = [book for book in sorted(
            library.books, key=lambda b: b.score) if book not in books_already_done]
        if books_by_score:
            output.append([library])
            output[-1].extend(reversed(books_by_score))
            books_already_done.extend(books_by_score)

    return output


def solve_2(books, libraries, days):
    output = []
    available_libs = list(libraries)
    books_already_done = []
    import random
    for i in range(len(libraries)):
        rand_index = random.randrange(len(available_libs))
        rand_lib = available_libs[rand_index]
        del available_libs[rand_index]
        books_by_score = [book for book in sorted(
            rand_lib.books, key=lambda b: b.score) if book not in books_already_done]
        if books_by_score:
            output.append([rand_lib])
            output[-1].extend(reversed(books_by_score))
            books_already_done.extend(books_by_score)

    return output


def solve(books, libraries, days):
    looking_for_laziest_library = True
    # A list of lists.
    # In each list, store the library followed by ids of books
    output = []
    book_frequency_dict = Counter(books)
    processed_lib_ids = []

    for i in range(len(libraries)):
        looking_for_laziest_library = not looking_for_laziest_library

        if looking_for_laziest_library:
            laziest_library = Library(-1, 0, 0, 0)
            for libr in libraries:
                if libr.id not in processed_lib_ids:
                    if libr.sign_up_time > laziest_library.sign_up_time:
                        laziest_library = libr
                    elif libr.sign_up_time == laziest_library.sign_up_time:
                        if libr.score > laziest_library.score:
                            laziest_library = libr

            output.append([laziest_library])
            # Slam all the books in there, biggest scorer first
            books_by_score = sorted(
                laziest_library.books, key=lambda b: b.score)

            output[-1].extend(reversed(books_by_score))
            processed_lib_ids.append(laziest_library.id)
        else:
            sweatiest_library = Library(-1, 0, 100001, 0)
            for libr in libraries:
                if libr.id not in processed_lib_ids:
                    if libr.sign_up_time < sweatiest_library.sign_up_time:
                        sweatiest_library = libr
                    elif libr.sign_up_time == sweatiest_library.sign_up_time:
                        if libr.score > sweatiest_library.score:
                            sweatiest_library = libr

            output.append([sweatiest_library])
            # Slam all the books in there, biggest scorer first
            books_by_score = sorted(
                sweatiest_library.books, key=lambda b: b.score)
            output[-1].extend(reversed(books_by_score))
            processed_lib_ids.append(sweatiest_library.id)

    return output


def main(filename):
    """Main function."""
    num_of_days = 0
    num_of_books = 0
    num_of_libraries = 0

    all_books = []
    libraries = []

    print_output = False

    # If the script is not executed with the filename as a parameter, get a
    # filename from the user.
    if not filename:
        filename = input("Please enter a filename:\n")

    print("Parsing input...")
    with open(filename) as f:
        # Parse the first line containing num of books, days and libraries.
        num_of_books, num_of_libraries, num_of_days = [
            int(x) for x in f.readline().split(" ")]

        # Parse the book scores into a comprehensive list of books.
        for idx, book_score in enumerate(f.readline().split(" ")):
            all_books.append(Book(int(book_score), idx))

        # Parse in all the libraries, and the books they hold.
        for i in range(num_of_libraries):
            library_info = [int(x) for x in f.readline().split(" ")]
            library_books = [int(y) for y in f.readline().split(" ")]

            # Add the library.
            libraries.append(
                Library(i, library_info[0], library_info[1], library_info[2]))

            # Update the books in the library.
            for book_id in library_books:
                # Add a reference to the book using the book id.
                libraries[i].books.append(all_books[book_id])

            # Calculate score for library.
            libraries[i].calculate_score()

        print("Input parsed!")

    print("Solving EPIC STYLE...")
    output = solve_3(all_books, libraries, num_of_days)
    num_of_libraries_signed_up = len(output)
    print("Solved!")

    # Print output
    if (print_output):
        for library in output:
            print(f"Library {str(library[0].id)} scans books: ", end="")
            for i in range(1, len(library)):
                print(str(library[i].id), end=" ")
            print()

    print("Writing output to file...")
    with open(filename.replace(".txt", "_output.txt"), "w") as f:
        # Write the number of libraries that are signed up.
        f.write(str(num_of_libraries_signed_up))
        f.write("\n")

        # Then, for each library signed up, write the id and number of books:
        for library in output:
            f.write(f"{library[0].id} {str(len(library) - 1)}\n")
            # Followed by the ids of books scanned.
            for i in range(1, len(library)):
                f.write(f"{library[i].id} ")
            f.write("\n")

    print("File output complete!")


#
if __name__ == "__main__":
    # If there is a filename argument, pass it to the main function.
    try:
        main(sys.argv[1])
    except:
        main(None)
