from dto.root_brood import *
from dto.root_translation import *
from SberTMT.model import TMT_obj
import pandas as pd


def experiment_ru_en(report_file, root_file, num_broods, num_contains, l_tm, r_tm, l_test, r_test):
    total_stats = []
    text_bleus = []
    root_bleus = []
    for n in range(num_broods):
        print(f"Start for {n}")
        brood = create_random_root_blood(num_contains, TM_TRASH_FILE, TEST_TRASH_FILE, l_tm, r_tm, l_test, r_test)
        brood_translation = RootTranslation(brood, TMT_obj, Language.RU, Language.EN)
        expanded_sources = [_s.ru.root_highlighted_as_translation for _s in brood.contains]
        text_bleu = brood_translation.avg_text_bleu
        root_bleu = brood_translation.avg_root_bleu
        text_bleus.append(text_bleu)
        root_bleus.append(root_bleu)
        roots = brood_translation.translated_roots
        pretty_formated = brood_translation.pretty_formated_translation
        stat = {
            "n": n,
            "avg_text_bleu": sum(text_bleus) / (n + 1),
            "avg_root_bleus": sum(root_bleus) / (n + 1)
        }
        total_stats.append(stat)
        stat_df = pd.DataFrame(data=total_stats)
        stat_df.to_csv(report_file)

        with open(root_file, "a", encoding='utf-8') as report:
            report.write("=" * 40)
            report.write("\n\n<br><br><b>RU root: </b><br>\n")
            report.write(brood.root.ru.text)
            report.write("\n\n<br><br><b>EN root: </b><br>\n")
            report.write(brood.root.en.text)

            report.write("\n\n<br><br><b>EXPANDED ROOTS: </b><br>\n")
            for i, _expanded in enumerate(expanded_sources):
                report.write(f"{str(i).zfill(3)}: {_expanded}")
                report.write("<br>\n")

            report.write("\n\n<br><br><b>ROOTS in translations: </b><br>\n")
            for i, _root in enumerate(roots):
                report.write(f"{str(i).zfill(3)}: {_root}")
                report.write("<br>\n")

            report.write("\n\n<br><b>PRETTY FORMATED: </b><br>\n")
            for i, _pretty in enumerate(pretty_formated):
                report.write(f"{str(i).zfill(3)}: {_pretty}")
                report.write("<br>\n")



if __name__ == "__main__":
    # brood = create_random_root_blood(10, TM_TRASH_FILE, TEST_TRASH_FILE, 1, 1, 1, 1)
    # brood_translation = RootTranslation(brood, TMT_obj, Language.RU, Language.EN)
    # tb = brood_translation.avg_text_bleu
    # rb = brood_translation.avg_root_bleu
    # roots = brood_translation.translated_roots
    # formated = brood_translation.formated_translation
    # print(tb)
    # print(rb)
    # print(roots)
    # print(formated)
    # a = 7
    name = "10_10_1111"
    experiment_ru_en(f"results/2021-12-02/{name}.csv", f"results/2021-12-02/{name}.txt", 10, 10, 1, 1, 1, 1)