import re
from symbols import *
from jointable import JoinTable
from category import Category

class Phrase:
      """Class for modeling the paired items that characterize the aligned approach to composition."""

      def __init__(self, *args):
            if len(args) == 1:
                  self.__build_from_xml(args[0])
            else:
                  self.__build_from_args(args)

      def __build_from_args(self, args):
            prem, conc, mcat, lex, projs = args
            self.prem  = prem
            self.conc  = conc
            self.mcat  = mcat
            self.pcat  = str(self.mcat)
            self.lex   = lex
            self.projs = projs

      def __build_from_xml(self, xml):
            fields_dict = self.__process_fields(xml)            
            if "lem" in fields_dict:
                  self.__build_refl_xml(fields_dict)
            else:
                  self.__build_pair_xml(fields_dict)
            
      def __build_refl_xml(self, fields_dict):  
            self.prem  = fields_dict["lem"]
            self.conc  = fields_dict["lem"]
            self.pcat  = fields_dict["pcat"]
            self.mcat  = Category(self.pcat)
            self.lex   = EQUALITY            
            self.projs = self.__build_projectivity_functions(fields_dict["proj"])

      def __build_pair_xml(self, fields_dict):            
            self.prem  = fields_dict["prem"]
            self.conc  = fields_dict["conc"]
            self.pcat  = fields_dict["pcat"]
            self.mcat  = Category(self.pcat)
            self.lex   = fields_dict["lex"]
            self.projs = self.__build_projectivity_functions(fields_dict["proj"])

      def __process_fields(self, xml):
            """Initial processing of an XML string into the components
            of a Phrase.  The tricky part is ensuring that multiple
            <proj> tags are processed correctly."""
            # Strip off the <item> delimiters.
            xml = re.sub(r"\s*</?item>\s*\n?", "", xml)
            # Process the fields into a dictionary.            
            field_re = re.compile(r"<(\w+)(?:\sn=([0-9]+))?>\s*(.*?)\s*</\1>", re.MULTILINE | re.DOTALL)
            fields = field_re.findall(xml)
            fields_dict = {}
            fields_dict["proj"] = {}
            for vals in fields:
                  if vals[0] == "proj":
                        index = 1
                        if vals[1]:
                              index = int(vals[1])
                        if index in fields_dict["proj"]:
                              raise Exception("Repeated projectivity index in %s" % xml)
                        # Add the current proj value at index.
                        if vals[2]:
                              fields_dict["proj"][index] = vals[2]
                  else:
                        # The simpler, non-proj cases.
                        fields_dict[vals[0]] = vals[2]
            # Proj: Create an array value as ordered by the dictionary's indices.
            fields_dict["proj"] = [x[1] for x in sorted(fields_dict["proj"].items())]
            return fields_dict

      def __build_projectivity_functions(self, proj_list):
            """Phrases can have multiple projectivity arguments.  This function
            parses them as specified by the XML format, which gives a list of
            <proj n=N> tags, where the Ns are sequential and unique and N=1 can
            be left off."""
            projs = []
            for proj_str in proj_list:
                  proj_str = proj_str.replace(" ", "")
                  # Split into pairs.
                  proj_str_pairs = proj_str.split(",")
                  # Split the pairs on the colon separator.
                  proj_pairs = map((lambda x : x.split(":")), proj_str_pairs)
                  # Turn into a function.
                  proj_dict = dict(proj_pairs)
                  # Check that the input was actually a function.
                  if len(proj_pairs) != len(proj_dict):
                        raise Exception("Value for <proj> was not functional; multiple values specified for the same input: %s" % fields["proj"])
                  # Check that all the elements in the dictionary are actually relations.
                  for key,val in proj_dict.items():
                        if key not in RELS:
                              raise Exception("Problem with projectivity: key %s is not a lexical relation.")
                        if val not in RELS:
                              raise Exception("Problem with projectivity: value %s is not a lexical relation.")            
                  projs.append(proj_dict)
            if len(projs) == 0:
                  projs = [DEFAULT_PROJ]
            return projs

      def __proj2str(self, proj):
            """Convert dictionary to format k:v,k:v,..."""
            proj_strs = []
            for key, val in proj.items():
                  proj_strs.append("%s:%s" % (key, val))
            return ", ".join(proj_strs)

      def to_xml(self):
            """Duplicates the style of the dictionary XML."""
            proj_xmls = []
            for i, p in enumerate(self.projs):
                  proj_str = self.__proj2str(p)
                  proj_xmls.append("\t<proj n=%s> %s </proj>" % (i+1, proj_str))
            # Where there is no projectivity, insert an empty tag.
            if len(proj_xmls) == 0:
                  proj_xmls = ["\t<proj n=1></proj>"]
            # Central XML.
            s = "<item>\n"
            s += "\t<prem>%s</prem>\n" % self.prem
            s += "\t<conc>%s</conc>\n" % self.conc
            s += "\t<pcat>%s</pcat>\n" % self.pcat
            s += "\t<lex>%s</lex>\n"   % self.lex
            s += "%s\n"                % "\n".join(proj_xmls)
            s += "</item>\n"
            return s

      def __str__(self):
            return self.to_xml()

      def __eq__(self, other):
            """Two phrases are equal iff they have all the same attributes."""
            return self.__dict__ == other.__dict__

      def __ne__(self, other):
            """Two phrases are not equal iff they have at least one differing attribute."""
            return self.__dict__ != other.__dict__
