from collections import Counter
import sys


# import results

def urls_out_links_counter(listOfPairs):
    """
    Counts the out-links number of each page into a dictionary that maps a URL to its out-links number.
    :param listOfPairs: list of pairs(also list). each pair [src, dest] is a link from page 'src' to page 'dest'.
    :return out_links: a dictionary where the keys are URLs and the values are the out-going links number of each URL.
    """

    out_links = Counter([src for src, _ in listOfPairs])  # Counts and creates the dictionary.
    for _, dest in listOfPairs:
        # Add pages without outgoing links (or discovered but not crawled pages) with a value of 0.
        out_links[dest] = out_links.get(dest, 0)
    return out_links


def is_diff_lt_epsilon(dict1, dict2):
    """
    Checks for each key if the difference between dict1[key] and dict2[key] less than epsilon.
    :param dict1: the first dictionary.
    :param dict2: the second dictionary.
    :return True iff the difference of each k-th pair less then epsilon, and False otherwise.
    """

    # epsilon = sys.float_info.epsilon
    epsilon = 0.00000000001
    if len(dict1) != len(dict2):  # i.e. the keys of dict1 and dict2 are different.
        return False
    for k in dict1.keys():
        if abs(dict1[k] - dict2[k]) > epsilon:
            return False
    return True


def pageRank(listOfPairs, numIters):
    """
    The function will use iterative update rules to compute a PageRank Score for each URL page.
    :param listOfPairs: list of pairs(also list). each pair [src, dest] is a link from page 'src' to page 'dest'.
    :param numIters: the number of times the update loop repeats itself.
    :return a dictionary where the keys are URLs and the values are the final score of each URL.
    """

    out_links_count = urls_out_links_counter(listOfPairs)
    num_of_urls = len(out_links_count)
    damping_factor = 0.8

    # Initialize page ranks to be (1 / N) for every page URL. (N = num_of_urls)
    curr_scores = dict((url, (1 / num_of_urls)) for url in out_links_count.keys())  # curr_scores also known as R(t+1).
    prev_scores = None

    less_than_epsilon_flag = False  # Helps prevent unnecessary checks if the ranking process converges.
    # The main scores update loop. occurs numIters times.
    for i in range(numIters):
        prev_scores = curr_scores.copy()  # prev_scores also known as R(t).

        # Iterate through each page URL and update its PageRank Score.
        for url in out_links_count.keys():
            # Calculate the formula: 0.8 * ∑src→dest (Rsrc(t) / Dsrc).
            # The main part of the score gets from pages linking to it, based on their score in the previous iteration.
            in_coming_links_score = damping_factor * sum(
                (prev_scores[src] / out_links_count[src]) for src, dest in listOfPairs if dest == url)

            # Calculate the formula: 0.2 * (1 / N).
            # Helps to prevent Spider-traps(all out-links are within the group), by random teleports.
            random_teleports_score = (1 - damping_factor) * (1 / num_of_urls)

            # Calculate the formula: 0.8 * ∑key∈deadEnds (Rkey(t) / N).
            # In cases of Dead-ends, there will always be a random teleports so the score will be divided equally between all the pages.
            dead_ends_score = damping_factor * sum(
                (prev_scores[key] / num_of_urls) for key, val in out_links_count.items() if val == 0)

            # R𝑗(t+1)
            curr_scores[url] = in_coming_links_score + random_teleports_score + dead_ends_score

        # check if the ranking process converges.
        if not less_than_epsilon_flag and is_diff_lt_epsilon(curr_scores, prev_scores):
            less_than_epsilon_flag = True

            # print(curr_scores)
            # print(prev_scores)
            # print('\n***The ranking process converge in:', i, '-th iteration***')

    # print(prev_scores)
    # print(curr_scores)
    # print(f'The sum of all scores is: {sum(v for v in curr_scores.values())}')
    return curr_scores


################## Main ##################

# 'links' is a list of pairs. each pair [src, dest] is a link from page 'src' to page 'dest'.

# links = [
#     ["abc", "def"],
#     ["abc", "ghi"],
#     ["def", "jkl"],
#     ["jkl", "mnop"],
#     ["mnop", "abc"],
#     ["mnop", "def"],
#     ["mnop", "ghi"]
# ]

# links = [
#     ['https://en.wikipedia.org/wiki/Feliciano_L%C3%B3pez', 'https://en.wikipedia.org/wiki/Marc_L%C3%B3pez'],
#     ['https://en.wikipedia.org/wiki/Bob_Bryan', 'https://en.wikipedia.org/wiki/Feliciano_L%C3%B3pez'],
#     ['https://en.wikipedia.org/wiki/Andy_Ram', 'https://en.wikipedia.org/wiki/Bob_Bryan'],
#     ['https://en.wikipedia.org/wiki/Carsten_Ball', 'https://en.wikipedia.org/wiki/Travis_Rettenmaier'],
#     ['https://en.wikipedia.org/wiki/Santiago_Gonz%C3%A1lez_(tennis)', 'https://en.wikipedia.org/wiki/Carsten_Ball'],
#     ['https://en.wikipedia.org/wiki/Martin_Emmrich', 'https://en.wikipedia.org/wiki/Santiago_Gonz%C3%A1lez_(tennis)'],
#     ['https://en.wikipedia.org/wiki/Maximilian_Neuchrist', 'https://en.wikipedia.org/wiki/James_Cluskey'],
#     ['https://en.wikipedia.org/wiki/Hugo_Nys', 'https://en.wikipedia.org/wiki/Maximilian_Neuchrist'],
#     ['https://en.wikipedia.org/wiki/Jonathan_Erlich', 'https://en.wikipedia.org/wiki/Hugo_Nys'],
#     ['https://en.wikipedia.org/wiki/Radek_%C5%A0t%C4%9Bp%C3%A1nek', 'https://en.wikipedia.org/wiki/Vasek_Pospisil'],
#     ['https://en.wikipedia.org/wiki/Ji%C5%99%C3%AD_Nov%C3%A1k',
#      'https://en.wikipedia.org/wiki/Radek_%C5%A0t%C4%9Bp%C3%A1nek'],
#     ['https://en.wikipedia.org/wiki/Wayne_Black', 'https://en.wikipedia.org/wiki/Ji%C5%99%C3%AD_Nov%C3%A1k'],
#     ['https://en.wikipedia.org/wiki/Mark_Petchey', 'https://en.wikipedia.org/wiki/Piet_Norval'],
#     ['https://en.wikipedia.org/wiki/Olivier_Dela%C3%AEtre', 'https://en.wikipedia.org/wiki/Mark_Petchey'],
#     ['https://en.wikipedia.org/wiki/Daniel_Nestor', 'https://en.wikipedia.org/wiki/Olivier_Dela%C3%AEtre'],
#     ['https://en.wikipedia.org/wiki/Luis_Horna', 'https://en.wikipedia.org/wiki/Jaroslav_Levinsk%C3%BD'],
#     ['https://en.wikipedia.org/wiki/Oliver_Marach', 'https://en.wikipedia.org/wiki/Luis_Horna'],
#     ['https://en.wikipedia.org/wiki/Jarkko_Nieminen', 'https://en.wikipedia.org/wiki/Oliver_Marach'],
#     ['https://en.wikipedia.org/wiki/%C4%A2irts_Dzelde', 'https://en.wikipedia.org/wiki/Jorge_Lozano'],
#     ['https://en.wikipedia.org/wiki/Udo_Plamberger', 'https://en.wikipedia.org/wiki/%C4%A2irts_Dzelde'],
#     ['https://en.wikipedia.org/wiki/Leander_Paes', 'https://en.wikipedia.org/wiki/Udo_Plamberger'],
#     ['https://en.wikipedia.org/wiki/%C3%93scar_Hern%C3%A1ndez_(tennis)', 'https://en.wikipedia.org/wiki/Mariano_Hood'],
#     ['https://en.wikipedia.org/wiki/Rub%C3%A9n_Ram%C3%ADrez_Hidalgo',
#      'https://en.wikipedia.org/wiki/%C3%93scar_Hern%C3%A1ndez_(tennis)'],
#     ['https://en.wikipedia.org/wiki/Pavel_V%C3%ADzner',
#      'https://en.wikipedia.org/wiki/Rub%C3%A9n_Ram%C3%ADrez_Hidalgo'],
#     ['https://en.wikipedia.org/wiki/Wesley_Moodie', 'https://en.wikipedia.org/wiki/Chris_Haggard'],
#     ['https://en.wikipedia.org/wiki/Agust%C3%ADn_Calleri', 'https://en.wikipedia.org/wiki/Wesley_Moodie'],
#     ['https://en.wikipedia.org/wiki/Stephen_Huss_(tennis)', 'https://en.wikipedia.org/wiki/Agust%C3%ADn_Calleri'],
#     ['https://en.wikipedia.org/wiki/Jonathan_Marray', 'https://en.wikipedia.org/wiki/Igor_Sijsling'],
#     ['https://en.wikipedia.org/wiki/Marin_Draganja', 'https://en.wikipedia.org/wiki/Jonathan_Marray'],
#     ['https://en.wikipedia.org/wiki/Mariusz_Fyrstenberg', 'https://en.wikipedia.org/wiki/Marin_Draganja'],
#     ['https://en.wikipedia.org/wiki/Mikael_Tillstr%C3%B6m', 'https://en.wikipedia.org/wiki/Alex_Radulescu'],
#     ['https://en.wikipedia.org/wiki/Kevin_Ullyett', 'https://en.wikipedia.org/wiki/Mikael_Tillstr%C3%B6m'],
#     ['https://en.wikipedia.org/wiki/Simone_Bolelli', 'https://en.wikipedia.org/wiki/Bj%C3%B6rn_Phau'],
#     ['https://en.wikipedia.org/wiki/Mike_Bryan', 'https://en.wikipedia.org/wiki/Simone_Bolelli'],
#     ['https://en.wikipedia.org/wiki/Sabine_Lisicki', 'https://en.wikipedia.org/wiki/Marion_Bartoli'],
#     ['https://en.wikipedia.org/wiki/Marion_Bartoli', 'https://en.wikipedia.org/wiki/Sabine_Lisicki'],
#     ['https://en.wikipedia.org/wiki/Venus_Williams', 'https://en.wikipedia.org/wiki/Marion_Bartoli'],
#     ['https://en.wikipedia.org/wiki/Andrea_Arnaboldi', 'https://en.wikipedia.org/wiki/Morgan_Phillips_(tennis)'],
#     ['https://en.wikipedia.org/wiki/Alexander_Kudryavtsev', 'https://en.wikipedia.org/wiki/Andrea_Arnaboldi'],
#     ['https://en.wikipedia.org/wiki/Ross_Hutchins', 'https://en.wikipedia.org/wiki/Alexander_Kudryavtsev'],
#     ['https://en.wikipedia.org/wiki/Joan_Balcells', 'https://en.wikipedia.org/wiki/Mauricio_Hadad'],
#     ['https://en.wikipedia.org/wiki/Lucas_Arnold', 'https://en.wikipedia.org/wiki/Joan_Balcells'],
#     ['https://en.wikipedia.org/wiki/Simon_Aspelin', 'https://en.wikipedia.org/wiki/Lucas_Arnold'],
#     ['https://en.wikipedia.org/wiki/Guillermo_Ca%C3%B1as', 'https://en.wikipedia.org/wiki/Todd_Reid'],
#     ['https://en.wikipedia.org/wiki/Andy_Roddick', 'https://en.wikipedia.org/wiki/Guillermo_Ca%C3%B1as'],
#     ['https://en.wikipedia.org/wiki/Robin_S%C3%B6derling',
#      'https://en.wikipedia.org/wiki/2009_French_Open_%E2%80%93_Men%27s_singles_final'],
#     ['https://en.wikipedia.org/wiki/Jonas_Bj%C3%B6rkman', 'https://en.wikipedia.org/wiki/Robin_S%C3%B6derling'],
#     ['https://en.wikipedia.org/wiki/Li_Na', 'https://en.wikipedia.org/wiki/Vera_Zvonareva'],
#     ['https://en.wikipedia.org/wiki/Sun_Tiantian', 'https://en.wikipedia.org/wiki/Li_Na'],
#     ['https://en.wikipedia.org/wiki/Mahesh_Bhupathi', 'https://en.wikipedia.org/wiki/Sun_Tiantian'],
#     ['https://en.wikipedia.org/wiki/Javier_Frana', 'https://en.wikipedia.org/wiki/Thomas_Enqvist'],
#     ['https://en.wikipedia.org/wiki/Marc-Kevin_Goellner', 'https://en.wikipedia.org/wiki/Javier_Frana'],
#     ['https://en.wikipedia.org/wiki/Max_Mirnyi', 'https://en.wikipedia.org/wiki/Marc-Kevin_Goellner'],
#     ['https://en.wikipedia.org/wiki/Ryan_Harrison', 'https://en.wikipedia.org/wiki/Matthew_Ebden'],
#     ['https://en.wikipedia.org/wiki/Nicholas_Monroe', 'https://en.wikipedia.org/wiki/Ryan_Harrison'],
#     ['https://en.wikipedia.org/wiki/Philipp_Petzschner', 'https://en.wikipedia.org/wiki/Nicholas_Monroe'],
#     ['https://en.wikipedia.org/wiki/Victor_Crivoi', 'https://en.wikipedia.org/wiki/Daniel_Elsner'],
#     ['https://en.wikipedia.org/wiki/Andreas_Seppi', 'https://en.wikipedia.org/wiki/Victor_Crivoi'],
#     ['https://en.wikipedia.org/wiki/Dominic_Thiem', 'https://en.wikipedia.org/wiki/Stefanos_Tsitsipas'],
#     ['https://en.wikipedia.org/wiki/Alexander_Zverev_Jr.', 'https://en.wikipedia.org/wiki/Dominic_Thiem'],
#     ['https://en.wikipedia.org/wiki/Alexander_Peya', 'https://en.wikipedia.org/wiki/Alexander_Zverev_Jr.'],
#     ['https://en.wikipedia.org/wiki/Xu_Yifan', 'https://en.wikipedia.org/wiki/Mallory_Burdette'],
#     ['https://en.wikipedia.org/wiki/Laura_Siegemund', 'https://en.wikipedia.org/wiki/Xu_Yifan'],
#     ['https://en.wikipedia.org/wiki/Vera_Zvonareva', 'https://en.wikipedia.org/wiki/Laura_Siegemund']
# ]
#
# final_scores = pageRank(links, 100)
# max = max(list(final_scores.values()))
# print(max, [url for url in final_scores.keys() if final_scores[url] == max])
